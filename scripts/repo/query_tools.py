#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--use-case",required=True); p.add_argument("--os",default="Windows 11"); p.add_argument("--arch",default="x64"); a=p.parse_args()
    tools=json.loads((ROOT/"tools/catalog.yaml").read_text(encoding="utf-8"))
    q=a.use_case.lower()
    rows=[t for t in tools if q in (t["category"]+" "+" ".join(t["use_cases"])+" "+t["name"]).lower() and t["status"]!="eol"]
    order={"Microsoft":0}; rows.sort(key=lambda t:(order.get(t["publisher"],1),{"R0":0,"R1":1,"R2":2,"R3":3,"R4":4}[t["risk_class"]],t["name"]))
    print(json.dumps({"query":vars(a),"results":rows[:12]},ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
