#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
REQUIRED=["intake.yaml","authorization.md","inventory.json","symptoms.md","timeline.jsonl","hypotheses.yaml","actions.jsonl","rollback.md"]
def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--case",required=True); a=p.parse_args(); root=Path(a.case)
    missing=[x for x in REQUIRED if not (root/x).exists()]
    secret_hits=[]
    for path in root.rglob("*"):
        if path.is_file() and path.stat().st_size<2_000_000:
            text=path.read_text(encoding="utf-8",errors="ignore").lower()
            if "recoverypassword" in text or "password=" in text or "token=" in text: secret_hits.append(str(path))
    print(json.dumps({"case":str(root),"missing":missing,"secret_warning_files":secret_hits,"valid":not missing and not secret_hits},indent=2))
    return 0 if not missing and not secret_hits else 1
if __name__=="__main__": raise SystemExit(main())
