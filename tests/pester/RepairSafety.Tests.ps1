$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Repair wrapper safety' {
 It 'generates plans only in default Scan mode' {
  $scripts=Get-ChildItem (Join-Path $Repo 'scripts\repair') -Filter 'Invoke-*.ps1'|Where-Object Name -ne 'Invoke-BootRepair.ps1'
  foreach($script in $scripts){
   $log=Join-Path $TestDrive $script.BaseName
   & $script.FullName -LogRoot $log -Synthetic
   if(-not(Test-Path -LiteralPath $log)){throw "Missing log root for $($script.Name)"}
   if(@(Get-ChildItem -LiteralPath $log -Filter '*-plan.json').Count -ne 1){throw "Expected one plan for $($script.Name)"}
   if(Test-Path -LiteralPath (Join-Path $log 'repair-actions.jsonl')){throw "Apply action log created in Scan: $($script.Name)"}
  }
 }
 It 'keeps Boot repair in Plan with fixture-safe volumes' {
  $log=Join-Path $TestDrive 'boot'
  & (Join-Path $Repo 'scripts\repair\Invoke-BootRepair.ps1') -Mode Plan -OsVolume D: -SystemVolume S: -Firmware UEFI -LogRoot $log -Synthetic
  if(-not(Test-Path (Join-Path $log 'boot-files-bcd-plan.json'))){throw 'Boot plan missing'}
 }
}
