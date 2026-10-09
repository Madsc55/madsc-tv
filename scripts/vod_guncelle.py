#!/usr/bin/env python3
"""Fetch TVMaze episode schedule metadata; never change CALISANLAR.m3u."""
import json, urllib.request, datetime, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
out=root/"vod"/"guncel-bolumler.json"
today=datetime.date.today()
records=[]
for delta in range(-7,8):
    day=(today+datetime.timedelta(days=delta)).isoformat()
    url="https://api.tvmaze.com/schedule?country=TR&date="+day
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"MadscTV-VOD-Metadata/1.0"})
        with urllib.request.urlopen(req,timeout=20) as response:
            episodes=json.load(response)
        for ep in episodes:
            show=ep.get("show") or {}
            records.append({"show":show.get("name"),"episode":ep.get("name"),"season":ep.get("season"),"number":ep.get("number"),"airdate":ep.get("airdate"),"url":ep.get("url"),"watch_url":None})
    except Exception as exc:
        print("Skipped",day,str(exc))
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({"updated":today.isoformat(),"note":"Bölüm yayın takvimi; oynatma bağlantısı değildir.","episodes":records},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("Episodes",len(records))
