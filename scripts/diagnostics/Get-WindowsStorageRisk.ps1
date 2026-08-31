<#
.SYNOPSIS Classifies storage telemetry without running filesystem or surface repairs.
.EXAMPLE .\Get-WindowsStorageRisk.ps1 -FixturePath .\tests\fixtures\storage\critical.json -OutputPath .\dist\storage-risk.json
#>
[CmdletBinding()]
param([string]$FixturePath,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
if($FixturePath){$storageInput=Get-Content -LiteralPath (Resolve-Path -LiteralPath $FixturePath) -Raw|ConvertFrom-Json}
else{
 if($PSVersionTable.PSVersion.Major -ge 6 -and -not $IsWindows){throw 'Live collection requires Windows.'}
 $storageInput=[ordered]@{disks=@(Get-Disk|Select-Object Number,FriendlyName,SerialNumber,HealthStatus,OperationalStatus,Size);physical=@(Get-PhysicalDisk|ForEach-Object{$d=$_;$r=$null;try{$r=$d|Get-StorageReliabilityCounter}catch{Write-Verbose "Reliability query failed for $($d.FriendlyName): $($_.Exception.Message)"};[pscustomobject]@{FriendlyName=$d.FriendlyName;HealthStatus=$d.HealthStatus;OperationalStatus=$d.OperationalStatus;Temperature=$r.Temperature;ReadErrorsTotal=$r.ReadErrorsTotal;WriteErrorsTotal=$r.WriteErrorsTotal;Wear=$r.Wear}})}
}
$serialized=$storageInput|ConvertTo-Json -Depth 10
$stopPatterns='(?i)critical|unhealthy|lost communication|read.?error[^0-9]*[1-9]|click|disappear|media error'
$cautionPatterns='(?i)warning|degraded|temperature[^0-9]*(?:[6-9][0-9]|1[0-9]{2})|wear[^0-9]*(?:9[0-9]|100)'
$classification=if($serialized -match $stopPatterns){'stop'}elseif($serialized -match $cautionPatterns){'caution'}else{'no-stop-signal-observed'}
$result=[ordered]@{schema_version='1.0.0';classification=$classification;rule='Absence of telemetry is not proof of health';do_not=@('chkdsk /f first on suspected physical failure','surface scan before image');evidence=$storageInput}
Write-WmJson $result $OutputPath
$result
