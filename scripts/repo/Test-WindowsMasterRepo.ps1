<#
.SYNOPSIS Runs safe repository validation, schema/static tests, Pester when compatible, packaging and temp install/uninstall.
.EXAMPLE .\Test-WindowsMasterRepo.ps1 -Category All
#>
[CmdletBinding()]
param([ValidateSet('All','Structure','Scripts','Safety','Links','Evals','Pester','Smoke')][string]$Category='All',[string]$ReportPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if(-not $ReportPath){$ReportPath=Join-Path $repo 'dist\reports\validation.json'}
New-Item -ItemType Directory -Path (Split-Path -Parent $ReportPath) -Force|Out-Null
$results=@()
function Add-Result([string]$Name,[string]$Status,[string]$Detail,[double]$Seconds){$script:results+=[pscustomobject][ordered]@{name=$Name;status=$Status;detail=$Detail;seconds=[Math]::Round($Seconds,3)}}
$failed=$false
if($Category -in @('All','Structure','Scripts','Safety','Links','Evals')){
 $sw=[Diagnostics.Stopwatch]::StartNew()
 & python (Join-Path $repo 'scripts\repo\validate_repo.py') --root $repo --category $Category --json-out (Join-Path $repo 'dist\reports\static-validation.json')
 $code=$LASTEXITCODE;$sw.Stop()
 if($code -eq 0){Add-Result 'static-validator' 'PASS' "category=$Category" $sw.Elapsed.TotalSeconds}else{Add-Result 'static-validator' 'FAIL' "exit=$code" $sw.Elapsed.TotalSeconds;$failed=$true}
}
if($Category -in @('All','Pester')){
 $pester=Get-Module -ListAvailable Pester|Sort-Object Version -Descending|Select-Object -First 1
 if(-not $pester){Add-Result 'Pester' 'SKIP' 'Pester is not installed; CI pins Pester 5.6.1.' 0}
 elseif($pester.Version.Major -lt 5){
  Import-Module Pester -RequiredVersion $pester.Version -Force
  $sw=[Diagnostics.Stopwatch]::StartNew()
  $pesterResult=Invoke-Pester -Script (Join-Path $repo 'tests\pester') -PassThru
  $sw.Stop()
  if($pesterResult.FailedCount -eq 0){Add-Result 'Pester' 'PASS' "$($pesterResult.PassedCount) passed with compatible local Pester $($pester.Version)" $sw.Elapsed.TotalSeconds}else{Add-Result 'Pester' 'FAIL' "$($pesterResult.FailedCount) failed with local Pester $($pester.Version)" $sw.Elapsed.TotalSeconds;$failed=$true}
 }
 else{
  Import-Module Pester -MinimumVersion 5.5 -Force
  $sw=[Diagnostics.Stopwatch]::StartNew()
  $config=New-PesterConfiguration
  $config.Run.Path=Join-Path $repo 'tests\pester'
  $config.Run.PassThru=$true;$config.Output.Verbosity='Detailed'
  $pesterResult=Invoke-Pester -Configuration $config;$sw.Stop()
  if($pesterResult.FailedCount -eq 0){Add-Result 'Pester' 'PASS' "$($pesterResult.PassedCount) passed" $sw.Elapsed.TotalSeconds}else{Add-Result 'Pester' 'FAIL' "$($pesterResult.FailedCount) failed" $sw.Elapsed.TotalSeconds;$failed=$true}
 }
}
$analyzer=Get-Module -ListAvailable PSScriptAnalyzer|Sort-Object Version -Descending|Select-Object -First 1
if($Category -in @('All','Scripts')){
 if(-not $analyzer){Add-Result 'PSScriptAnalyzer' 'SKIP' 'Module not installed; AST safety/style checks ran in static-validator; CI pins 1.24.0.' 0}
 else{
  Import-Module PSScriptAnalyzer -Force
  $sw=[Diagnostics.Stopwatch]::StartNew()
  $issues=@(Invoke-ScriptAnalyzer -Path (Join-Path $repo 'scripts') -Recurse -Settings (Join-Path $repo 'PSScriptAnalyzerSettings.psd1'));$sw.Stop()
  if($issues.Count -eq 0){Add-Result 'PSScriptAnalyzer' 'PASS' '0 findings' $sw.Elapsed.TotalSeconds}else{Add-Result 'PSScriptAnalyzer' 'FAIL' "$($issues.Count) findings" $sw.Elapsed.TotalSeconds;$failed=$true}
 }
}
if($Category -in @('All','Smoke')){
 $sw=[Diagnostics.Stopwatch]::StartNew()
 $packageRoot=Join-Path $repo 'dist\skills'
 & (Join-Path $repo 'scripts\repo\Build-SkillPackages.ps1') -Destination $packageRoot|Out-Null
 $temp=Join-Path $repo 'dist\test-install'
 if(Test-Path -LiteralPath $temp){Remove-Item -LiteralPath $temp -Recurse -Force}
 & (Join-Path $repo 'scripts\repo\Install-WindowsMasterSkills.ps1') -Destination $temp -Source (Join-Path $repo '.agents\skills') -Mode Copy|Out-Null
 $installed=@(Get-ChildItem -LiteralPath $temp -Directory|Where-Object Name -notmatch '^\.').Count
 & (Join-Path $repo 'scripts\repo\Uninstall-WindowsMasterSkills.ps1') -Destination $temp -Confirm:$false|Out-Null
 $remaining=@(Get-ChildItem -LiteralPath $temp -Directory -ErrorAction SilentlyContinue|Where-Object Name -notmatch '^\.').Count
 $sw.Stop()
 if($installed -eq 39 -and $remaining -eq 0){Add-Result 'package-install-uninstall-smoke' 'PASS' '39 installed, 0 remaining' $sw.Elapsed.TotalSeconds}else{Add-Result 'package-install-uninstall-smoke' 'FAIL' "installed=$installed remaining=$remaining" $sw.Elapsed.TotalSeconds;$failed=$true}
}
$summary=[ordered]@{created_utc=[DateTime]::UtcNow.ToString('o');host_powershell=$PSVersionTable.PSVersion.ToString();category=$Category;results=$results;passed=@($results|Where-Object status -eq 'PASS').Count;failed=@($results|Where-Object status -eq 'FAIL').Count;skipped=@($results|Where-Object status -eq 'SKIP').Count}
$summary|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $ReportPath -Encoding utf8
$results|Format-Table -AutoSize
if($failed){exit 1}else{exit 0}
