$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Fixture-safe collectors' {
 It 'classifies critical storage as stop and healthy fixture without a stop signal' {
  $critical=Join-Path $TestDrive 'critical.json';$safe=Join-Path $TestDrive 'safe.json'
  $c=& (Join-Path $Repo 'scripts\diagnostics\Get-WindowsStorageRisk.ps1') -FixturePath (Join-Path $Repo 'tests\fixtures\storage\critical.json') -OutputPath $critical
  $s=& (Join-Path $Repo 'scripts\diagnostics\Get-WindowsStorageRisk.ps1') -FixturePath (Join-Path $Repo 'tests\fixtures\storage\safe.json') -OutputPath $safe
  if($c.classification -ne 'stop'){throw "Critical storage was $($c.classification)"}
  if($s.classification -eq 'stop'){throw 'Safe fixture classified as stop'}
 }
 It 'maps a synthetic UEFI layout without assuming C' {
  $out=Join-Path $TestDrive 'boot.json'
  $result=& (Join-Path $Repo 'scripts\diagnostics\Get-WindowsBootLayout.ps1') -FixturePath (Join-Path $Repo 'tests\fixtures\boot\uefi.json') -OutputPath $out
  if($result.rule -notmatch 'never assume C'){throw 'Missing WinRE drive-letter rule'}
 }
 It 'runs every generic collector against a synthetic fixture' {
  $cases=@(
   @('Export-WindowsRelevantEvents.ps1','tests\fixtures\update.json'),
   @('Get-WindowsDriverInventory.ps1','tests\fixtures\drivers.json'),
   @('Get-WindowsUpdateHealth.ps1','tests\fixtures\update.json'),
   @('Get-WindowsStartupPersistence.ps1','tests\fixtures\persistence.json'),
   @('Get-WindowsNetworkSnapshot.ps1','tests\fixtures\network.json'),
   @('Get-BitLockerSafetyStatus.ps1','tests\fixtures\bitlocker.json'),
   @('Get-WindowsManagementStatus.ps1','tests\fixtures\management.json')
  )
  foreach($case in $cases){
   $out=Join-Path $TestDrive ($case[0]+'.json')
   & (Join-Path $Repo ('scripts\diagnostics\'+$case[0])) -FixturePath (Join-Path $Repo $case[1]) -OutputPath $out|Out-Null
   if(-not(Test-Path -LiteralPath $out)){throw "Collector did not create output: $($case[0])"}
   $data=Get-Content -LiteralPath $out -Raw|ConvertFrom-Json
   if($data.source -ne 'fixture'){throw "Collector source mismatch: $($case[0])"}
  }
 }
 It 'extracts minidump metadata without claiming a diagnosis' {
  $out=Join-Path $TestDrive 'dump.json'
  $result=& (Join-Path $Repo 'scripts\diagnostics\Get-MinidumpMetadata.ps1') -Path (Join-Path $Repo 'tests\fixtures\dumps\synthetic.dmp.txt') -OutputPath $out
  if($result.analysis -ne 'metadata-only'){throw 'Dump parser overclaims analysis'}
 }
}
