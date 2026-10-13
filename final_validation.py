"""Separate priority continuity audit; never modifies playlists or prior checks."""
import concurrent.futures
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess

OUT = pathlib.Path('madsc_son_kontrol')

def progress_number(values, name):
    try:
        return max(0, int(values.get(name, '0')))
    except (ValueError, TypeError):
        return 0

def assess(returncode, progress, duration):
    values = dict(line.split('=', 1) for line in progress.splitlines() if '=' in line)
    seconds = progress_number(values, 'out_time_us') / 1000000
    frames = progress_number(values, 'frame')
    return {'passed': returncode == 0 and seconds >= duration - 1 and frames > 1,
            'decoded_seconds': seconds, 'decoded_frames': frames}

def audit(candidate, duration):
    url = candidate['url']
    token = hashlib.sha256(url.encode()).hexdigest()[:20]
    result = {'candidate_id': token, 'label': candidate['label'],
              'selection_reason': candidate['reason'],
              'source_id': candidate.get('source_id', ''),
              'source_language_hint': candidate.get('source_language_hint', 'UNKNOWN'),
              'license_status': 'NOT_VERIFIED',
              'source_rights_review': 'REQUIRED',
              'station_identity_evidence': 'NOT_VERIFIED',
              'logo_identity_evidence': 'NOT_VERIFIED',
              'epg_device_evidence': 'NOT_VERIFIED',
              'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'station_identity': 'REVIEW_REQUIRED', 'ibo_sweden': 'NOT_VERIFIED'}
    try:
        probe = subprocess.run(['ffprobe', '-v', 'error', '-rw_timeout', '12000000',
                                '-show_streams', '-of', 'json', url],
                               capture_output=True, text=True, timeout=35)
        streams = json.loads(probe.stdout or '{}').get('streams', [])
        result['video'] = [{k: s.get(k) for k in ('codec_name', 'width', 'height', 'avg_frame_rate')}
                           for s in streams if s.get('codec_type') == 'video']
        result['audio'] = [{k: s.get(k) for k in ('codec_name', 'sample_rate', 'channels')}
                           for s in streams if s.get('codec_type') == 'audio']
        p = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'info',
                            '-rw_timeout', '12000000', '-i', url, '-t', str(duration),
                            '-map', '0:v:0', '-map', '0:a:0',
                            '-vf', 'freezedetect=n=-50dB:d=5,blackdetect=d=5:pix_th=0.10',
                            '-af', 'silencedetect=n=-50dB:d=5',
                            '-progress', 'pipe:1', '-f', 'null', '-'],
                           capture_output=True, text=True, timeout=duration + 90)
        result['continuity'] = assess(p.returncode, p.stdout, duration)
        result['review_events'] = {name: len(re.findall(pattern, p.stderr))
                                   for name, pattern in [('freeze', r'freeze_start:'),
                                                         ('black', r'black_start:'),
                                                         ('silence', r'silence_start:')]}
        # Events can be normal programme content, so never certify identity or reject solely on them.
        result['status'] = 'TECHNICAL_PASS_IDENTITY_PENDING' if result['continuity']['passed'] else 'CONTINUITY_FAILED'
        if any(result['review_events'].values()) and result['continuity']['passed']:
            result['status'] = 'TECHNICAL_PASS_CONTENT_REVIEW'
        frame = OUT / 'images' / (token + '.jpg')
        thumb = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error',
                                '-rw_timeout', '12000000', '-i', url, '-frames:v', '1',
                                '-vf', 'scale=640:-2', '-y', str(frame)],
                               capture_output=True, timeout=35)
        result['image_evidence'] = str(frame) if thumb.returncode == 0 and frame.exists() else None
    except subprocess.TimeoutExpired:
        result['status'] = 'TIMEOUT'
    except (ValueError, OSError):
        result['status'] = 'PROBE_OR_DECODER_ERROR'
    return result

def turkish_priority(candidate):
    """Only explicit Turkish identity metadata earns first priority; names alone are unsafe."""
    country = str(candidate.get('country', '')).lower()
    language = str(candidate.get('source_language_hint', '')).lower()
    source_id = str(candidate.get('source_id', '')).lower()
    label = str(candidate.get('label', '')).casefold()
    if country == 'tr' or language == 'tur' or source_id in ('iptv-org-tr', 'iptv-org-turkiye', 'dearbulut-tr', 'iptv-org-turkce', 'dearbulut-turkce'):
        return 0
    if 'türk' in label or 'turk' in label:
        return 0
    if country in ('az', 'cy', 'tm'):
        return 1
    return 2

def pending_candidates(manifest, state, results):
    """Never repeat a recorded final check, including failures or timeouts."""
    completed = {r['candidate_id'] for r in results}
    candidates = {hashlib.sha256(r['url'].encode()).hexdigest()[:20]: r
                  for r in manifest['candidates']}
    for record in state.values():
        checks = record.get('checks', [])
        if len(checks) != 3 or not all(c['passed'] for c in checks):
            continue
        token = hashlib.sha256(record['url'].encode()).hexdigest()[:20]
        candidates.setdefault(token, {'url': record['url'], 'label': record['channel'],
            'reason': 'Three separate decode passes; identity and device still unverified',
            'source_id': record.get('source_id', ''),
            'source_language_hint': record.get('source_language_hint', 'UNKNOWN'),
            'source_history': record.get('source_history', [])})
    pending = [r for token, r in candidates.items() if token not in completed]
    return sorted(pending, key=turkish_priority)

BATCH_SIZE = 125  # Kullanici onayli dengeli grup: onceki 200 adaydan daha kisa.
MAX_WORKERS = 24  # Kullanici onayli paralel islem sayisi.

def main():
    manifest = json.loads(pathlib.Path('final_validation_manifest.json').read_text())
    (OUT / 'images').mkdir(parents=True, exist_ok=True)
    resultfile = OUT / 'results.json'
    results = json.loads(resultfile.read_text()) if resultfile.exists() else []
    state = json.loads(pathlib.Path('madsc_dogrulama/state.json').read_text())['channels']
    candidates = pending_candidates(manifest, state, results)
    batch = candidates[:BATCH_SIZE]
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(audit, r, manifest['duration_seconds']) for r in batch]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            resultfile.write_text(json.dumps(results, ensure_ascii=False, indent=2))
            print(json.dumps({'label': result['label'], 'status': result['status']}, ensure_ascii=False), flush=True)
    summary = {'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
               'scope': 'Resumable completed-candidate batches; previous results preserved.',
               'selected_this_run': len(batch), 'remaining': max(0, len(candidates)-len(batch)),
               'selected': len(results),
               'completed': len(results), 'requested_seconds': manifest['duration_seconds'],
               'status_counts': {s: sum(r['status'] == s for r in results) for s in sorted({r['status'] for r in results})},
               'ready_for_playlist': 0,
               'identity_and_device_confirmation_required': True,
               'playlist_blob': manifest['playlist_blob'], 'three_stage_state_blob': manifest['state_blob']}
    (OUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
