"""Persistent candidate verification; never writes playlists or discovery history."""
import concurrent.futures, datetime as dt, json, pathlib, subprocess
from madsc_akilli_kesif import key

OUT = pathlib.Path('madsc_dogrulama')
GAP = dt.timedelta(hours=6)

def eligible(record, now):
    checks = record.get('checks', [])
    if len(checks) >= 3:
        return False
    return not checks or now - dt.datetime.fromisoformat(checks[-1]['time']) >= GAP

def decode(url):
    command = ['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error',
               '-rw_timeout', '12000000', '-i', url, '-t', '30',
               '-map', '0:v:0', '-map', '0:a:0', '-progress', 'pipe:1',
               '-f', 'null', '-']
    try:
        p = subprocess.run(command, capture_output=True, text=True, timeout=80)
        values = dict(line.split('=', 1) for line in p.stdout.splitlines() if '=' in line)
        try:
            seconds = int(values.get('out_time_us', '0')) / 1000000
            frames = int(values.get('frame', '0'))
        except (ValueError, TypeError):
            return {'passed': False, 'seconds': 0, 'frames': 0,
                    'error': 'INVALID_PROGRESS'}
        return {'passed': p.returncode == 0 and seconds >= 29 and frames > 0,
                'seconds': seconds, 'frames': frames,
                'error': '' if p.returncode == 0 else 'DECODE_ERROR'}
    except subprocess.TimeoutExpired:
        return {'passed': False, 'error': 'TIMEOUT'}

def main():
    OUT.mkdir(exist_ok=True)
    statefile = OUT / 'state.json'
    state = json.loads(statefile.read_text()) if statefile.exists() else {'channels': {}}
    history = json.loads(pathlib.Path('madsc_kesif/gecmis.json').read_text())['history']
    # Merge unseen wide-scan candidates without modifying existing checks.\n    review_path = pathlib.Path('madsc_genis_tarama/candidate_review.json')\n    if review_path.exists():\n        review = json.loads(review_path.read_text(encoding='utf-8'))['candidates']\n        if not isinstance(review, dict):\n            raise ValueError('Invalid wide-scan review queue')\n        for candidate in review.values():\n            if candidate.get('status') != 'IDENTITY_REVIEW_REQUIRED_NOT_TESTED':\n                continue\n            url = candidate['url']\n            identity = key(url)\n            if identity not in history:\n                state['channels'].setdefault(identity, {\n                    'channel': candidate['name'], 'url': url, 'checks': [],\n                    'identity': 'NOT_VERIFIED', 'ibo_sweden': 'NOT_VERIFIED',\n                    'source': candidate['source'], 'origin': 'WIDE_SOURCE_SCAN'})\n    for identity, candidate in history.items():
        if candidate.get('successful_runs', 0) > 0:
            state['channels'].setdefault(identity, {'channel': candidate['channel'],
                'url': candidate['url'], 'checks': [], 'identity': 'NOT_VERIFIED',
                'ibo_sweden': 'NOT_VERIFIED'})
    now = dt.datetime.now(dt.timezone.utc)
    due = sorted((k for k, v in state['channels'].items() if eligible(v, now)),
                 key=lambda k: (len(state['channels'][k]['checks']), k))[:240]
    def one(identity):
        result = decode(state['channels'][identity]['url'])
        result['time'] = dt.datetime.now(dt.timezone.utc).isoformat()
        return identity, result
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for identity, result in pool.map(one, due):
            state['channels'][identity]['checks'].append(result)
    now = dt.datetime.now(dt.timezone.utc)
    records = list(state['channels'].values())
    summary = {'time': now.isoformat(), 'candidates': len(records), 'tested_this_run': len(due),
               'due_now': sum(eligible(r, now) for r in records),
               'waiting_6h': sum(bool(r['checks']) and len(r['checks']) < 3 and not eligible(r, now) for r in records),
               'failed': sum(bool(r['checks']) and not r['checks'][-1]['passed'] for r in records),
               'three_decode_passes': sum(len(r['checks']) == 3 and all(c['passed'] for c in r['checks']) for r in records),
               'completed_three_attempts': sum(len(r['checks']) == 3 for r in records),
               'pass_distribution': {str(n): sum(len(r['checks']) == 3 and sum(c['passed'] for c in r['checks']) == n for r in records) for n in range(4)},
               'ready_for_playlist': 0,
               'limits': ['Decode success does not verify station identity, freezing, or Sweden IBO playback. Identity and device confirmation remain required.']}
    temporary = OUT / 'state.tmp'
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    temporary.replace(statefile)
    (OUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False))

if __name__ == '__main__':
    main()
