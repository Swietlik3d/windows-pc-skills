$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Synthetic parsers' {
 It 'extracts servicing and setup errors without changing fixtures' {
  $cbs=Join-Path $TestDrive 'cbs.json';$setup=Join-Path $TestDrive 'setup.json'
  & (Join-Path $Repo 'scripts\diagnostics\Parse-WindowsServicingLog.ps1') -Path (Join-Path $Repo 'tests\fixtures\logs\CBS.log') -OutputPath $cbs|Out-Null
  & (Join-Path $Repo 'scripts\diagnostics\Parse-WindowsSetupLog.ps1') -Path (Join-Path $Repo 'tests\fixtures\logs\setuperr.log') -OutputPath $setup|Out-Null
  if((Get-Content $cbs -Raw|ConvertFrom-Json).matched_count -le 0){throw 'CBS parser returned no matches'}
  $setupResult=Get-Content $setup -Raw|ConvertFrom-Json
  if(@($setupResult.hits).Count -le 0){throw 'Setup parser returned no hits'}
 }
}
