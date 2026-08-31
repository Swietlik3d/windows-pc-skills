<#
.SYNOPSIS Produces a read-only boot-layout map; it never selects, formats, or writes a partition.
.EXAMPLE .\Get-WindowsBootLayout.ps1 -FixturePath .\tests\fixtures\boot\uefi.json -OutputPath .\dist\boot-layout.json
#>
[CmdletBinding()]
param([string]$FixturePath,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
if($FixturePath){$data=Get-Content -LiteralPath (Resolve-Path -LiteralPath $FixturePath) -Raw|ConvertFrom-Json;$source='fixture'}
else{
 if($PSVersionTable.PSVersion.Major -ge 6 -and -not $IsWindows){throw 'Live collection requires Windows.'}
 $fw='unknown';try{$fw=(Get-ComputerInfo -Property BiosFirmwareType).BiosFirmwareType}catch{Write-Verbose "Firmware query failed: $($_.Exception.Message)"}
 $data=[ordered]@{firmware=$fw;disks=@(Get-Disk|Select-Object Number,UniqueId,FriendlyName,PartitionStyle,Size,IsBoot,IsSystem);partitions=@(Get-Partition|Select-Object DiskNumber,PartitionNumber,DriveLetter,Type,GptType,IsActive,IsBoot,IsSystem,Size);volumes=@(Get-Volume|Select-Object DriveLetter,FileSystemLabel,FileSystem,HealthStatus,Size,SizeRemaining)}
 $source='live-read-only'
}
$result=[ordered]@{schema_version='1.0.0';source=$source;rule='OS volume requires Windows directory + SOFTWARE hive + BCD corroboration; never assume C:';data=$data}
Write-WmJson $result $OutputPath
$result
