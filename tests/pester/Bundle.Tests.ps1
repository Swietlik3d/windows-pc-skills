$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Repair bundle fixture path' {
 It 'creates redacted JSON, Markdown, HTML, manifest and ZIP' {
  $root=Join-Path $TestDrive 'bundle'
  & (Join-Path $Repo 'scripts\diagnostics\Get-WindowsRepairBundle.ps1') -Mode Basic -FixtureRoot (Join-Path $Repo 'tests\fixtures\repair-bundle') -OutputPath $root
  if($LASTEXITCODE -ne 0){throw "Bundle exit code $LASTEXITCODE"}
  foreach($path in @("$root\manifest.json","$root\summary.md","$root\summary.html","$root.zip")){if(-not(Test-Path -LiteralPath $path)){throw "Missing $path"}}
  if((Get-Content "$root\os.json" -Raw) -match 'alice@example'){throw 'E-mail was not redacted'}
 }
}
