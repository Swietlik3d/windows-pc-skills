#!/usr/bin/env python3
"""Static, dependency-free router over the checked-in symptom index."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents" / "skills"

def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-ząćęłńóśźż0-9]{3,}", value.lower()))

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    query = tokens(args.text)
    high_risk = {
        "storage": ["klika", "clicking", "znika", "smart", "read error"],
        "physical": ["spuchnię", "swollen", "spaleniz", "burning", "ciecz", "liquid"],
        "encryption": ["bitlocker", "recovery key", "herstelcode"],
        "managed": ["firma", "company", "mdm", "entra", "domain"],
    }
    lower=args.text.lower()
    risk_text=re.sub(r"\b(?:nie|not|geen)\s+(?:dysk\s+)?(?:klika|clicking|znika|disappear\w*)\b","",lower)
    flags = [key for key, words in high_risk.items() if any(word in risk_text for word in words)]
    scores = []
    for skill_md in SKILLS.glob("*/SKILL.md"):
        if skill_md.parent.name == "_shared":
            continue
        text = skill_md.read_text(encoding="utf-8")
        description_match = re.search(r'^description:\s*"?(.+?)"?$', text, re.M)
        haystack = tokens((description_match.group(1) if description_match else "") + " " + skill_md.parent.name)
        score = len(query & haystack)
        if score:
            scores.append((score, skill_md.parent.name))
    scores.sort(key=lambda item: (-item[0], item[1]))
    if not scores or scores[0][0] < 2:
        primary = "windows-master-router"
        supporting = []
        confidence = "low"
    else:
        primary = scores[0][1]
        supporting = [name for _, name in scores[1:4] if name != primary]
        confidence = "high" if scores[0][0] >= 4 else "medium"
    if "storage" in flags:
        primary = "storage-triage-cloning-recovery"
        supporting = [name for name in ["windows-case-evidence", "pc-hardware-diagnostics"] if name != primary]
    primary_file=SKILLS/primary/"SKILL.md"
    if primary_file.exists():
        related=re.findall(r"\[`([a-z0-9-]+)`\]\(\.\./[a-z0-9-]+/SKILL\.md\)",primary_file.read_text(encoding="utf-8"))
        if related:
            supporting=[name for name in dict.fromkeys(related) if name!=primary][:3]
    result = {
        "primary": primary,
        "supporting": supporting[:3],
        "confidence": confidence,
        "safety_flags": flags,
        "required_gates": ["boot state", "backup", "BitLocker", "management", "data value"],
        "first_step": "R0 evidence only; stop on red flags",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
