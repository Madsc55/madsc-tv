"""Collect bounded on-air frames for failed logo URLs; never infer a visual match."""
import concurrent.futures
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'logo_deneme/visual_frames'

def capture(item):
    name, url = item
    filename = hashlib.sha256(name.encode()).hexdigest()[:20] + '.jpg'
    target = OUT / filename
    target.unlink(missing_ok=True)
    try:
        result = subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error',
            '-rw_timeout','8000000','-i',url,'-frames:v','1','-vf','scale=960:-1',
            '-y',str(target)],capture_output=True,timeout=30)
        success = result.returncode == 0 and target.exists()
    except (subprocess.TimeoutExpired, OSError):
        success = False
    if not success:
        target.unlink(missing_ok=True)
    return {'channel':name,'frame':filename if success else None,
        'status':'FRAME_READY_FOR_REVIEW' if success else 'FRAME_UNAVAILABLE_RETRY_NEXT_RUN',
        'visual_match':'NOT_VERIFIED'}

def main():
    audit = json.loads((ROOT/'logo_deneme/rapor.json').read_text())
    wanted = {e['name'] for e in audit['entries'] if e['status'] not in ('IMAGE_OK','SVG_XML_OK')}
    lines = (ROOT/'CALISANLAR.m3u').read_text().splitlines()
    jobs = {}
    for i,line in enumerate(lines[:-1]):
        if not line.startswith('#EXTINF'):
            continue
        name = line.rsplit(',',1)[-1].strip()
        if name not in wanted:
            continue
        base = re.sub(r'\s+\d+P(?:\s+(?:HD|FHD|SD|QHD))?$', '', name)
        base = re.sub(r'\s+\d+$','',base)
        jobs.setdefault(base,lines[i+1])
    OUT.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(capture,jobs.items()))
    (ROOT/'logo_deneme/visual_review.json').write_text(json.dumps({
        'checked_channels':len(results),'results':results,
        'limits':'A captured frame is evidence for review, not automatic proof of matching artwork.'},
        ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'channels':len(results),'frames_ready':sum(bool(r['frame']) for r in results)}))

if __name__ == '__main__':
    main()
