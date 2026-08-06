$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$ModulePath=Join-Path $Repo 'scripts\lib\WindowsMaster.HostAdapter.psm1'
Import-Module $ModulePath -Force
$ModuleName=(Get-Module|Where-Object Path -eq $ModulePath|Select-Object -First 1).Name

Describe 'Mocked read-only host boundaries' {
 It 'mocks registry reads' {
  Mock -CommandName Get-ItemProperty -ModuleName $ModuleName -MockWith {[pscustomobject]@{State='synthetic'}}
  $result=Get-WmRegistrySnapshot -LiteralPath 'HKLM:\SYNTHETIC'
  if($result.State -ne 'synthetic'){throw 'Registry mock result mismatch'}
  Assert-MockCalled -CommandName Get-ItemProperty -ModuleName $ModuleName -Times 1 -Exactly
 }
 It 'mocks service reads' {
  Mock -CommandName Get-Service -ModuleName $ModuleName -MockWith {[pscustomobject]@{Name='SyntheticService';Status='Stopped'}}
  $result=Get-WmServiceSnapshot -Name SyntheticService
  if($result.Status -ne 'Stopped'){throw 'Service mock result mismatch'}
  Assert-MockCalled -CommandName Get-Service -ModuleName $ModuleName -Times 1 -Exactly
 }
 It 'mocks BCD enumeration and DISM ScanHealth' {
  Mock -CommandName bcdedit.exe -ModuleName $ModuleName -MockWith {'synthetic-bcd'}
  Mock -CommandName dism.exe -ModuleName $ModuleName -MockWith {'synthetic-dism'}
  if((Get-WmBcdSnapshot) -notcontains 'synthetic-bcd'){throw 'BCD mock result mismatch'}
  if((Get-WmDismScanHealth) -notcontains 'synthetic-dism'){throw 'DISM mock result mismatch'}
  Assert-MockCalled -CommandName bcdedit.exe -ModuleName $ModuleName -Times 1 -Exactly
  Assert-MockCalled -CommandName dism.exe -ModuleName $ModuleName -Times 1 -Exactly
 }
 It 'mocks CIM and network reads' {
  Mock -CommandName Get-CimInstance -ModuleName $ModuleName -MockWith {[pscustomobject]@{Caption='Synthetic OS'}}
  Mock -CommandName Get-NetIPConfiguration -ModuleName $ModuleName -MockWith {[pscustomobject]@{InterfaceAlias='Synthetic NIC'}}
  if((Get-WmCimSnapshot -ClassName Win32_OperatingSystem).Caption -ne 'Synthetic OS'){throw 'CIM mock result mismatch'}
  if((Get-WmNetworkSnapshotBoundary).InterfaceAlias -ne 'Synthetic NIC'){throw 'Network mock result mismatch'}
  Assert-MockCalled -CommandName Get-CimInstance -ModuleName $ModuleName -Times 1 -Exactly
  Assert-MockCalled -CommandName Get-NetIPConfiguration -ModuleName $ModuleName -Times 1 -Exactly
 }
 It 'mocks filesystem reads' {
  Mock -CommandName Get-Content -ModuleName $ModuleName -MockWith {'synthetic-file'}
  if((Get-WmFileSnapshot -LiteralPath 'X:\synthetic.txt') -ne 'synthetic-file'){throw 'Filesystem mock result mismatch'}
  Assert-MockCalled -CommandName Get-Content -ModuleName $ModuleName -Times 1 -Exactly
 }
}
