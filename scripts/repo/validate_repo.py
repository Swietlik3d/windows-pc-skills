#!/usr/bin/env python3
"""Dependency-free structural, schema-shaped, link, safety and eval validation."""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, time
from pathlib import Path

EXPECTED_SKILLS = {
 "windows-master-router","windows-service-intake","windows-case-evidence","pc-hardware-diagnostics",
 "bios-uefi-firmware","storage-triage-cloning-recovery","memory-cpu-gpu-thermal","windows-os-identification",
 "windows-boot-recovery","winpe-offline-repair","windows-bcd-partition-repair","windows-component-repair",
 "windows-update-servicing","windows-setup-upgrade-rollback","windows-activation-licensing","windows-bsod-debugging",
 "windows-performance-hangs","windows-process-service-startup","windows-drivers-devices","windows-network-repair",
 "windows-peripherals-repair","windows-accounts-profiles","windows-ntfs-permissions-shares",
 "windows-bitlocker-tpm-security","windows-malware-remediation","windows-apps-store-winget",
 "windows-shell-ui-repair","windows-office-cloud-repair","windows-backup-vss-restore",
 "windows-remote-managed-client","windows-advanced-administration","windows-automation-powershell",
 "windows-deployment-imaging","windows-service-media","windows-legacy-xp-vista-7-8","windows-10-support",
 "windows-11-support","windows-post-repair-validation","windows-tool-research"
}
REQUIRED_HEADINGS = [
 "Cel i granice odpowiedzialności","Kiedy aktywować i kiedy nie aktywować",
 "Dane wejściowe i minimalne pytania bezpieczeństwa","Szybki triage i czerwone flagi",
 "Zgodność","Drzewo objaw","Najpierw diagnostyka read-only","Drabina napraw",
 "Karty poleceń","Dlaczego to może pójść źle","Backup i rollback","Oczekiwany wynik",
 "Walidacja i regresja","Przerwanie i eskalacja","Logi i artefakty","Powiązane skille",
 "Źródła","Antywzorce"
]
PLAYBOOK_FIELDS = {
 "id","title","summary","symptoms","applies_to","excludes","risk_class","authorization_required",
 "prerequisites","data_safety","evidence_to_collect","hypotheses","diagnostics","repair_ladder",
 "commands","rollback","validation","stop_conditions","escalation","related_skills","sources",
 "last_verified","status"
}
TOOL_FIELDS = {
 "id","name","category","publisher","official_home","official_download","official_repository",
 "current_version","checked_at","status","replaced_by","license","commercial_use","redistribution",
 "supported_os","architectures","environments","portable","install_type","network_required",
 "elevation_required","signature_method","checksum_method","risk_class","use_cases","avoid_when",
 "known_gotchas","alternatives","sources"
}
ORCHESTRATOR_METADATA_KEYS = {
 "swietlik.orchestrator.schema","swietlik.orchestrator.pack",
 "swietlik.orchestrator.recommended-agent","swietlik.orchestrator.minimum-agent",
 "swietlik.orchestrator.reasoning","swietlik.orchestrator.verbosity",
 "swietlik.orchestrator.delegation","swietlik.orchestrator.review",
 "swietlik.orchestrator.parallel","swietlik.orchestrator.risk"
}

class Check:
 def __init__(self):
  self.errors=[]; self.warnings=[]; self.metrics={}; self.checks=[]
 def error(self, msg): self.errors.append(msg)
 def warn(self, msg): self.warnings.append(msg)
 def record(self, name, before, started):
  self.checks.append({"name":name,"status":"PASS" if len(self.errors)==before else "FAIL","new_errors":len(self.errors)-before,"seconds":round(time.time()-started,3)})

def frontmatter(text):
 if not text.startswith("---\n"): return {}, ""
 end=text.find("\n---\n",4)
 if end<0:return {}, ""
 data={}; parent=None
 for line in text[4:end].splitlines():
  if ":" not in line:continue
  key,value=line.split(":",1)
  if line.startswith("  ") and parent=="metadata":
   data[parent][key.strip()]=value.strip().strip('"')
  else:
   parent=key.strip(); parsed=value.strip().strip('"')
   data[parent]={} if parent=="metadata" and not parsed else parsed
 return data,text[end+5:]

def load_json(path, c):
 try:return json.loads(path.read_text(encoding="utf-8"))
 except Exception as exc:c.error(f"JSON/YAML parse {path}: {exc}");return None

def structure(root,c):
 start=time.time();before=len(c.errors);base=root/".agents"/"skills"
 required_artifacts=[
  "AGENTS.md","README.md","LICENSE.md","SECURITY.md","CHANGELOG.md","ROADMAP.md","REPO_STATUS.md",
  "RESEARCH_QUEUE.md","coverage-matrix.yaml",".github/workflows/validate.yml",
  "knowledge-base/hardware/hardware-safety-gates.yaml","knowledge-base/security/security-gates.yaml",
  "docs/architecture.md","docs/operating-model.md","docs/diagnostic-method.md",
  "docs/safety-and-authorization.md","docs/source-policy.md","docs/tool-selection-policy.md",
  "docs/service-media.md","docs/legacy-isolation.md","docs/testing-lab.md","docs/maintenance.md",
  "docs/assumptions.md","tools/catalog.yaml","tools/catalog.schema.json"
 ]
 for rel in required_artifacts:
  if not (root/rel).exists():c.error(f"Missing required repository artifact: {rel}")
 actual={p.name for p in base.iterdir() if p.is_dir() and p.name!="_shared"}
 if actual!=EXPECTED_SKILLS:c.error(f"Skill set mismatch missing={sorted(EXPECTED_SKILLS-actual)} extra={sorted(actual-EXPECTED_SKILLS)}")
 if (base/"_shared"/"SKILL.md").exists():c.error("_shared must not contain SKILL.md")
 total_playbooks=total_cards=0
 for name in sorted(EXPECTED_SKILLS):
  folder=base/name; path=folder/"SKILL.md"
  if not path.exists():c.error(f"Missing {path}");continue
  text=path.read_text(encoding="utf-8");fm,body=frontmatter(text)
  if set(fm)!={"name","description","metadata"}:c.error(f"{name}: frontmatter keys {sorted(fm)}")
  if fm.get("name")!=name:c.error(f"{name}: name mismatch")
  metadata=fm.get("metadata",{})
  if not isinstance(metadata,dict) or set(metadata)!=ORCHESTRATOR_METADATA_KEYS:c.error(f"{name}: invalid orchestrator metadata keys")
  elif metadata.get("swietlik.orchestrator.schema")!="1" or metadata.get("swietlik.orchestrator.pack")!="windows-pc-skills":c.error(f"{name}: invalid orchestrator metadata identity")
  desc=fm.get("description","")
  if not 120<=len(desc)<=900:c.error(f"{name}: description length {len(desc)}")
  if not re.search(r"[ąćęłńóśźż]",desc.lower()) or "Use for" not in desc:c.error(f"{name}: description must contain Polish and English trigger language")
  if len(text.splitlines())>=500:c.error(f"{name}: SKILL.md >=500 lines")
  for heading in REQUIRED_HEADINGS:
   if heading not in body:c.error(f"{name}: missing heading/content {heading}")
  for rel in ["references/playbooks.md","references/command-cards.md","references/compatibility.md","references/sources.md","agents/openai.yaml","assets/validation-checklist.md"]:
   if not (folder/rel).exists():c.error(f"{name}: missing {rel}")
  pb=(folder/"references"/"playbooks.md").read_text(encoding="utf-8")
  cards=(folder/"references"/"command-cards.md").read_text(encoding="utf-8")
  pbc=len(re.findall(r"^## [a-z0-9-]+-pb-\d{2}:",pb,re.M)); cc=len(re.findall(r"^- \*\*ID:\*\* `[a-z0-9-]+-cmd-\d{2}`",cards,re.M))
  total_playbooks+=pbc;total_cards+=cc
  if pbc<3:c.error(f"{name}: only {pbc} playbooks")
  if cc<3:c.error(f"{name}: only {cc} command cards")
  yaml=(folder/"agents"/"openai.yaml").read_text(encoding="utf-8")
  m=re.search(r'  short_description: "(.*)"',yaml)
  if not m or not 25<=len(m.group(1))<=64:c.error(f"{name}: invalid short_description")
  if f"${name}" not in yaml:c.error(f"{name}: default_prompt does not mention skill")
 c.metrics.update({"skills":len(actual),"playbooks_in_skill_refs":total_playbooks,"command_cards_in_skill_refs":total_cards})
 c.record("structure",before,start)

def schemas(root,c):
 start=time.time();before=len(c.errors)
 for path in list(root.rglob("*.yaml"))+list(root.rglob("*.json")):
  if any(part in {".git","dist"} for part in path.parts):continue
  if path.name in {"openai.yaml","pack.yaml"}:continue
  load_json(path,c)
 playbooks=list((root/"knowledge-base"/"playbooks").glob("*.yaml"))
 sources=load_json(root/"knowledge-base"/"sources"/"source-register.yaml",c) or []
 source_ids={row.get("id") for row in sources if isinstance(row,dict)}
 for path in playbooks:
  row=load_json(path,c)
  if not isinstance(row,dict):continue
  missing=PLAYBOOK_FIELDS-set(row)
  if missing:c.error(f"{path}: missing {sorted(missing)}")
  if row.get("status") not in {"complete","partial","experimental","requires-live-validation"}:c.error(f"{path}: invalid status")
  for sid in row.get("sources",[]):
   if sid not in source_ids:c.error(f"{path}: unknown source {sid}")
 tools=load_json(root/"tools"/"catalog.yaml",c) or []
 ids=set()
 for row in tools:
  if set(row)!=TOOL_FIELDS:c.error(f"tool {row.get('id')}: fields mismatch missing={sorted(TOOL_FIELDS-set(row))} extra={sorted(set(row)-TOOL_FIELDS)}")
  if row.get("id") in ids:c.error(f"duplicate tool {row.get('id')}")
  ids.add(row.get("id"))
  if row.get("redistribution") not in {"forbidden","unknown","allowed","conditional"}:c.error(f"tool {row.get('id')}: redistribution")
  if not str(row.get("official_home","")).startswith("https://"):c.error(f"tool {row.get('id')}: non-HTTPS official home")
 c.metrics.update({"machine_playbooks":len(playbooks),"sources":len(sources),"tools":len(tools)})
 c.record("schema-shaped-data",before,start)

def links(root,c):
 start=time.time();before=len(c.errors);checked=0
 markdown=[p for p in root.rglob("*.md") if ".git" not in p.parts and "dist" not in p.parts and p.name!="prompt_codex_windows_master_service_skills.md"]
 pattern=re.compile(r"\[[^\]]*\]\(([^)]+)\)")
 for path in markdown:
  for target in pattern.findall(path.read_text(encoding="utf-8")):
   if target.startswith(("http://","https://","mailto:","#")):continue
   target=target.strip("<>").split("#",1)[0]
   if not target:continue
   checked+=1
   resolved=(path.parent/target).resolve()
   if not resolved.exists():c.error(f"Broken link {path.relative_to(root)} -> {target}")
 c.metrics["internal_links_checked"]=checked;c.record("internal-links",before,start)

def safety(root,c):
 start=time.time();before=len(c.errors)
 forbidden_ext={".exe",".dll",".iso",".wim",".esd",".ffu",".sys",".msi",".msix",".vhd",".vhdx",".pfx",".key"}
 bad_files=[str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and p.suffix.lower() in forbidden_ext and ".git" not in p.parts]
 if bad_files:c.error("Forbidden binary/media files: "+", ".join(bad_files))
 for path in (root/"scripts").rglob("*.ps1"):
  text=path.read_text(encoding="utf-8")
  if re.search(r"(?im)^\s*(Invoke-Expression|iex)\b|\b(?:irm|iwr|curl)\b[^\n|]*\|\s*(?:iex|sh|bash|powershell)",text):c.error(f"unsafe code execution pattern: {path}")
  if "Win32_Product" in text:c.error(f"Win32_Product in executable script: {path}")
  if path.parent.name=="repair":
   if "SupportsShouldProcess" not in text or "-Apply" not in text and "[switch]$Apply" not in text:c.error(f"repair safety gate incomplete: {path}")
   if re.search(r"(?im)ValidateSet\('Scan','Repair'\).*='Repair'",text):c.error(f"repair defaults to Repair: {path}")
 # Exact secret patterns, excluding the specification and redaction fixtures/pattern code.
 secret_patterns=[r"\bsk-[A-Za-z0-9_-]{20,}",r"\bAKIA[A-Z0-9]{16}\b",r"\b\d{6}(?:-\d{6}){7}\b"]
 excluded_placeholder_files={"prompt_codex_windows_master_service_skills.md","generate_repository.py","validate_repo.py","Structure.Tests.ps1"}
 for path in root.rglob("*"):
  if not path.is_file() or any(part in {".git","dist"} for part in path.parts) or path.name=="prompt_codex_windows_master_service_skills.md":continue
  if path.name in excluded_placeholder_files:continue
  if path.suffix.lower() not in {".md",".json",".yaml",".ps1",".psm1",".py",".cmd",".yml"}:continue
  text=path.read_text(encoding="utf-8",errors="ignore")
  if path.name in {"WindowsMaster.Common.psm1","validate_repo.py"}:continue
  for pat in secret_patterns:
   if re.search(pat,text):c.error(f"secret-like value in {path.relative_to(root)}")
 placeholders=[]
 for path in root.rglob("*"):
  if not path.is_file() or any(part in {".git","dist"} for part in path.parts) or path.name=="prompt_codex_windows_master_service_skills.md":continue
  if path.name in excluded_placeholder_files:continue
  if path.suffix.lower() in {".md",".ps1",".py",".yaml",".json"}:
   text=path.read_text(encoding="utf-8",errors="ignore")
   if re.search(r"(?i)TODO:\s*(add|complete|replace)|\[TODO",text):placeholders.append(str(path.relative_to(root)))
 if placeholders:c.error("Unresolved placeholders: "+", ".join(placeholders))
 c.metrics["forbidden_binary_count"]=len(bad_files);c.record("safety",before,start)

def evals(root,c):
 start=time.time();before=len(c.errors);files=list((root/"tests"/"evals").glob("*.yaml"));prompts=0
 expected_files=EXPECTED_SKILLS
 actual=set()
 for path in files:
  if path.name=="router-quality-rubric.yaml":continue
  row=load_json(path,c)
  if not isinstance(row,dict):continue
  actual.add(row.get("skill")); pos=row.get("positive",[]);neg=row.get("negative",[]);amb=row.get("ambiguous",[]);prompts+=len(pos)+len(neg)+len(amb)
  if len(pos)<12 or len(neg)<8 or len(amb)<4:c.error(f"{path}: eval counts {len(pos)}/{len(neg)}/{len(amb)}")
  for item in pos:
   if item.get("expected_primary")!=row.get("skill"):c.error(f"{path}: positive expected primary mismatch")
   if item.get("max_supporting",99)>3:c.error(f"{path}: too many supporting")
 if actual!=expected_files:c.error(f"eval skill set mismatch")
 coverage=load_json(root/"coverage-matrix.yaml",c) or []
 for row in coverage:
  if row.get("coverage")=="planned":c.error(f"planned coverage: {row.get('id')}")
  if not (root/row.get("playbook","")).exists():c.error(f"coverage missing playbook: {row.get('id')}")
 short=load_json(root/"examples"/"synthetic-cases"/"short-cases.yaml",c) or []
 full=list((root/"examples"/"synthetic-cases"/"full").glob("full-case-*.yaml"))
 if len(short)<60:c.error(f"short cases only {len(short)}")
 if len(full)<15:c.error(f"full cases only {len(full)}")
 c.metrics.update({"eval_files":len(actual),"eval_prompts":prompts,"coverage_rows":len(coverage),"short_cases":len(short),"full_cases":len(full)})
 c.record("evals-and-coverage",before,start)

def scripts(root,c):
 start=time.time();before=len(c.errors)
 ps=list((root/"scripts").rglob("*.ps1"))+list((root/"scripts").rglob("*.psm1"))
 required=["Install-WindowsMasterSkills.ps1","Uninstall-WindowsMasterSkills.ps1","Build-SkillPackages.ps1","Test-WindowsMasterRepo.ps1","Update-WindowsKnowledgeBase.ps1","Update-ToolCatalog.ps1","New-WindowsServiceCase.ps1","Add-WindowsCaseAction.ps1","New-WindowsServiceReport.ps1","Get-WindowsRepairBundle.ps1","Get-WindowsStorageRisk.ps1","Get-WindowsBootLayout.ps1","Export-WindowsRelevantEvents.ps1","Get-WindowsDriverInventory.ps1","Get-WindowsUpdateHealth.ps1","Get-WindowsStartupPersistence.ps1","Get-WindowsNetworkSnapshot.ps1","Get-BitLockerSafetyStatus.ps1","New-ServiceMediaPlan.ps1","Get-VerifiedServiceTool.ps1","Test-ServiceMediaIntegrity.ps1"]
 names={p.name for p in ps}
 for name in required:
  if name not in names:c.error(f"missing required script {name}")
 command=["pwsh","-NoProfile","-NonInteractive","-Command",r"$bad=@();Get-ChildItem -LiteralPath $env:WM_VALIDATE_SCRIPT_ROOT -Recurse -Include *.ps1,*.psm1|ForEach-Object{$e=$null;[System.Management.Automation.Language.Parser]::ParseFile($_.FullName,[ref]$null,[ref]$e)|Out-Null;if($e){$bad+=@($e|ForEach-Object{\"$($_.Extent.File):$($_.Extent.StartLineNumber):$($_.Message)\"})}};if($bad){$bad|Write-Error;exit 1}"]
 try:
  env=os.environ.copy();env["WM_VALIDATE_SCRIPT_ROOT"]=str(root/"scripts")
  proc=subprocess.run(command,capture_output=True,text=True,timeout=90,env=env)
  if proc.returncode!=0:c.error("PowerShell syntax parse: "+(proc.stderr or proc.stdout)[-4000:])
 except Exception as exc:c.error(f"PowerShell syntax parser unavailable: {exc}")
 c.metrics["powershell_files"]=len(ps);c.record("scripts",before,start)

def package_check(root,c):
 package_root=root/"dist"/"skills"
 if not package_root.exists():return
 start=time.time();before=len(c.errors);packages=[p for p in package_root.iterdir() if p.is_dir()]
 if packages and len(packages)!=39:c.error(f"package count {len(packages)}")
 for p in packages:
  if not (p/"SKILL.md").exists() or not (p/"references"/"_shared"/"schemas"/"playbook.schema.json").exists():c.error(f"package not self-contained: {p.name}")
 c.metrics["packages"]=len(packages);c.record("packages",before,start)

def main():
 p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--category",default="All");p.add_argument("--json-out");a=p.parse_args()
 root=Path(a.root).resolve();c=Check();cat=a.category.lower()
 if cat in {"all","structure"}:structure(root,c)
 if cat in {"all","structure"}:schemas(root,c)
 if cat in {"all","links"}:links(root,c)
 if cat in {"all","safety"}:safety(root,c)
 if cat in {"all","evals"}:evals(root,c)
 if cat in {"all","scripts"}:scripts(root,c)
 package_check(root,c)
 result={"status":"PASS" if not c.errors else "FAIL","errors":c.errors,"warnings":c.warnings,"metrics":c.metrics,"checks":c.checks}
 if a.json_out:
  out=Path(a.json_out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False,indent=2))
 return 0 if not c.errors else 1
if __name__=="__main__":raise SystemExit(main())
