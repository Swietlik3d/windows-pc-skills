$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Case lifecycle' {
 It 'creates, appends and reports without PII requirement' {
  $root=Join-Path $TestDrive 'cases'
  $case=& (Join-Path $Repo 'scripts\reporting\New-WindowsServiceCase.ps1') -Slug synthetic -OwnerAlias owner-001 -AuthorizationLevel R0 -Root $root -Date ([datetime]'2026-08-06')
  & (Join-Path $Repo 'scripts\reporting\Add-WindowsCaseAction.ps1') -CasePath $case -Purpose validation -RiskClass R0 -Result success -Rollback not-applicable|Out-Null
  $result=& (Join-Path $Repo 'scripts\reporting\New-WindowsServiceReport.ps1') -CasePath $case -RequireValidation
  if($result.Status -ne 'validated'){throw "Unexpected status $($result.Status)"}
  if(-not(Test-Path (Join-Path $case 'technical-report.md'))){throw 'Technical report missing'}
 }
}
