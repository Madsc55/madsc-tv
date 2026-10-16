#!/usr/bin/env python3
"""Run existing score/review scripts on K2 artifacts without additional probes."""
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

try:
    from scripts.discovery_history_restore import find_previous, gh_json
    from scripts import category_stability_history as stability
except ModuleNotFoundError:
    from discovery_history_restore import find_previous, gh_json
    import category_stability_history as stability

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['KANAL', 'ADAY_TURU', 'TEKNIK_MEDYA', 'SES_IZI', 'COZUNURLUK',
          'LOGO_ADAY_URL', 'YAYIN_URL', 'KAYNAK']


def write_csv(path, rows, fields=FIELDS):
    with path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_run(root):
    repo, branch, run_id = (os.environ[key] for key in
                            ('GITHUB_REPOSITORY', 'GITHUB_REF_NAME', 'GITHUB_RUN_ID'))
    run = gh_json(repo, 'actions/runs/' + run_id)
    if run.get('path') == '.github/workflows/madsc-05-genel-bakim.yml':
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        if (run.get('head_sha') != head or run.get('head_branch') != branch
                or (run.get('head_repository') or {}).get('full_name') != repo):
            raise ValueError('Unexpected parent run provenance')
        jobs = gh_json(repo, 'actions/runs/' + run_id + '/jobs?per_page=100')['jobs']
        discovery = [j for j in jobs if 'MADSC 02 - Kanal Kesfi Toplu' in j.get('name', '')]
        if len(discovery) != 1 or discovery[0].get('conclusion') != 'success':
            raise ValueError('Current K2 job has no successful acceptance')
        return run
    previous = find_previous(root, repo, branch, run_id)
    if previous is None:
        raise ValueError('No accepted discovery artifact is available')
    return previous


def build_reports(artifact, output, scripts=ROOT / 'scripts', history=None):
    candidate_file = artifact / 'madsc_kesif/adaylar.csv'
    with candidate_file.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if not {'kanal', 'url', 'video', 'ses', 'durum'} <= set(reader.fieldnames or []):
            raise ValueError('Candidate media schema missing')
        observed = list(reader)
    candidates, technical = [], []
    for item in observed:
        url = item.get('url', '')
        if not url.startswith(('https://', 'http://')):
            continue
        tested = item.get('durum') != 'SONRAKI_TEST_BEKLIYOR'
        if tested and any(item.get(field, '').lower() not in ('true', 'false') for field in ('video', 'ses')):
            raise ValueError('Test edilmis adayda acik video/ses sonucu yok')
        video = tested and item.get('video', '').lower() == 'true'
        audio = tested and item.get('ses', '').lower() == 'true'
        state = ('TEST_EDILMEDI' if not tested else 'VIDEO_SES_VAR' if video and audio
                 else 'YALNIZ_VIDEO' if video else 'YALNIZ_SES' if audio else 'DOGRULANAMADI')
        row = dict(KANAL=item.get('kanal', ''), ADAY_TURU='K2_ADAYI', TEKNIK_MEDYA=state,
                   SES_IZI=str(bool(audio)), COZUNURLUK=item.get('cozunurluk', '') if video else '',
                   LOGO_ADAY_URL='', YAYIN_URL=url, KAYNAK=item.get('kaynak', ''))
        candidates.append(row)
        if tested:
            technical.append(row)
    review_file = artifact / 'madsc_genis_tarama/candidate_review.json'
    if review_file.exists():
        review = json.loads(review_file.read_text(encoding='utf-8')).get('candidates')
        if not isinstance(review, dict) or any(not isinstance(v, dict) for v in review.values()):
            raise ValueError('Invalid identity review queue')
        for item in review.values():
            url = item.get('url', '')
            if url.startswith(('https://', 'http://')):
                candidates.append(dict(KANAL=item.get('name', ''), ADAY_TURU='KIMLIK_INCELEME',
                    TEKNIK_MEDYA='TEST_EDILMEDI', SES_IZI='', COZUNURLUK='', LOGO_ADAY_URL='',
                    YAYIN_URL=url, KAYNAK=item.get('source', '')))
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / 'YENILER_TARAMA_RAPORU.csv', candidates)
    write_csv(output / 'ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv', technical)
    stability_report = {'longitudinal_evidence': 'NOT_IMPORTED_NOT_VERIFIED'}
    if history is None:
        write_csv(output / 'KARARLILIK_RAPORU.csv', [], ['YAYIN_URL', '24_SAAT_KARARLI'])
    else:
        measured = stability.measured_rows(artifact, technical)
        history, stable_rows, counts = stability.track(measured, history, require_measurement_time=True)
        history_file = output / stability.NAME
        history_file.write_text(json.dumps(history, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        write_csv(output / 'KARARLILIK_RAPORU.csv', stable_rows, stability.FIELDS)
        stability_report = {'longitudinal_evidence': 'TIMESTAMPED_OBSERVATIONS_ONLY', **counts,
            'stability_history_channels': len(history),
            'stability_history_observations': sum(map(len, history.values())),
            'stability_history_sha256': hashlib.sha256(history_file.read_bytes()).hexdigest(),
            'stable_24h_current_candidates': sum(r['24_SAAT_KARARLI'] == 'EVET' for r in stable_rows),
            'stability_window_days': 7, 'latest_required_within_hours': 24,
            'continuous_playback_verified': False, '30_day_verification': False}

    subprocess.run([sys.executable, str(scripts / 'akilli_aday_puanla.py'),
                    'YENILER_TARAMA_RAPORU.csv', 'ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv'],
                   cwd=output, check=True)
    subprocess.run([sys.executable, str(scripts / 'birlesik_aday_raporu.py')], cwd=output, check=True)
    with (output / 'AKILLI_ADAY_PUANLARI.csv').open(encoding='utf-8-sig', newline='') as handle:
        scores = list(csv.DictReader(handle))
    with (output / 'BIRLESIK_ADAY_ONAY_RAPORU.csv').open(encoding='utf-8-sig', newline='') as handle:
        combined = list(csv.DictReader(handle))
    if len(scores) != len(combined):
        raise ValueError('Scoring and review coverage differ')
    if any(r['ANA_LISTEYE_EKLENEBILIR'] != 'HAYIR' or r['KIMLIK_DOGRULANDI'] != 'HAYIR' for r in scores):
        raise ValueError('Unexpected automatic score approval')
    if any(r['ANA_LISTEYE_EKLE'] != 'HAYIR' or r['IBO_ONAYI'] != 'YOK'
           or r['KULLANICI_ONAYI'] != 'YOK' for r in combined):
        raise ValueError('Unexpected automatic review approval')
    return {'candidate_input_rows': len(candidates), 'explicit_media_rows': len(technical),
            'scored_candidates': len(scores), 'review_candidates': len(combined),
            **stability_report, 'additional_media_probes': 0,
            'playlist_write': False, 'device_approval': False}


def main():
    run = source_run(ROOT)
    history, history_source = stability.restore(ROOT)
    with tempfile.TemporaryDirectory(prefix='madsc-score-input-') as tmp:
        subprocess.run(['gh', 'run', 'download', str(run['id']), '--repo',
                        os.environ['GITHUB_REPOSITORY'], '--name', 'madsc-kesif-tek-kosu-rapor',
                        '--dir', tmp], check=True, capture_output=True)
        report = build_reports(Path(tmp), ROOT / 'madsc_aday_puanlama', history=history)
    report.update(source_run_id=run['id'], source_commit=run['head_sha'], stability_history_source=history_source)
    (ROOT / 'madsc_aday_puanlama/kabul.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
