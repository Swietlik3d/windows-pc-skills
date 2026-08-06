#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, xml.etree.ElementTree as ET
from pathlib import Path
def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--path",required=True); a=p.parse_args(); path=Path(a.path)
    errors=[]; warnings=[]
    try: ET.parse(path)
    except Exception as exc: errors.append(str(exc))
    text=path.read_text(encoding="utf-8",errors="ignore")
    for pattern,label in [(r"(?i)<Password>","password element"),(r"(?i)<ProductKey>","product key element"),(r"(?i)<AutoLogon>","autologon")]:
        if re.search(pattern,text): warnings.append(label+" requires secret/redaction review")
    print(json.dumps({"path":str(path),"errors":errors,"warnings":warnings,"valid":not errors},indent=2)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
