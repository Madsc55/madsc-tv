#!/usr/bin/env python3
"""Read-only missing Turkish station watchlist. Never edits playlists or retests URLs."""
import json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGETS=[
 {"name":"Sözcü TV","aliases":["SÖZCÜ TV","SOZCU TV","SZC TV"]},
 {"name":"Akit TV","aliases":["AKİT TV","AKIT TV"]},
 {"name":"Kanal Samsun","aliases":["KANAL SAMSUN"]},
 {"name":"Samsun Haber","aliases":["SAMSUN HABER","SAMSUN HABER TV"]},
]
def norm(s):
 s=unicodedata.normalize("NFKD",s.casefold().replace("ı","i"))
 return re.sub(r"[^a-z0-9]","", "".join(c for c in s if not unicodedata.combining(c)))
def entries(text):
 for line in text.splitlines():
  if line.startswith("#EXTINF"):
   yield line.rsplit(",",1)[-1].strip()
def main():
 playlist=(ROOT/"CALISANLAR.m3u").read_text(encoding="utf-8-sig")
 present={norm(x) for x in entries(playlist)}
 source=ROOT/"madsc_kesif"/"gecmis.json"
 history={}
 history_warning=None
 if source.exists():
  try:
   raw=source.read_text(encoding="utf-8-sig").strip()
   data=json.loads(raw) if raw else None
   if isinstance(data,dict) and isinstance(data.get("history"),dict):
    history=data["history"]
   else:
    history_warning="History snapshot empty or invalid; no historical candidates inferred."
  except (OSError,ValueError):
   history_warning="History snapshot unreadable; no historical candidates inferred."
 result=[]
 for target in TARGETS:
  aliases={norm(x) for x in target["aliases"]}
  matches=[{"name":v.get("channel",""),"url":v.get("url",""),"successful_runs":v.get("successful_runs",0)} for v in history.values() if isinstance(v,dict) and norm(str(v.get("channel",""))) in aliases]
  result.append({"target":target["name"],"already_in_playlist":bool(aliases & present),"historical_candidates":matches,"confirmed_channel_identity":False,"status":"IDENTITY_AND_IBO_CHECK_REQUIRED" if matches else "SEARCH_REQUIRED"})
 print(json.dumps({"note":"Only exact-name candidate matching; not proof of station identity, Turkish audio, or stream uptime.","history_warning":history_warning,"targets":result},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
