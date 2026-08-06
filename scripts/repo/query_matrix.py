#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--os", required=True, choices=["windows-10","windows-11"]); p.add_argument("--build", required=True); a=p.parse_args()
    data=json.loads((ROOT/"knowledge-base/os/windows-release-matrix.yaml").read_text(encoding="utf-8"))
    key=a.os.replace("-","_")
    matches=[row for row in data[key] if str(a.build).startswith(row["build_family"])]
    print(json.dumps({"snapshot_date":data["snapshot_date"],"matches":matches,"source":data["source"]},ensure_ascii=False,indent=2))
    return 0 if matches else 2
if __name__=="__main__": raise SystemExit(main())
