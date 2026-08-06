<#
.SYNOPSIS Extracts safe file metadata from dump fixtures; it does not claim a WinDbg diagnosis.
.EXAMPLE .\Get-MinidumpMetadata.ps1 -Path .\tests\fixtures\dumps\synthetic.dmp.txt -OutputPath .\dist\dump.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Path,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot);Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$file=Get-Item -LiteralPath (Resolve-Path -LiteralPath $Path)
$bytes=[IO.File]::ReadAllBytes($file.FullName);$prefix=[BitConverter]::ToString($bytes[0..([Math]::Min(31,$bytes.Length-1))]).Replace('-','')
$result=[ordered]@{name=$file.Name;length=$file.Length;last_write_utc=$file.LastWriteTimeUtc.ToString('o');sha256=(Get-FileHash $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant();prefix_hex=$prefix;analysis='metadata-only';required_for_diagnosis='WinDbg with symbols and multiple correlated dumps'}
Write-WmJson $result $OutputPath;$result
