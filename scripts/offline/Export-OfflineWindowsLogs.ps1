<#
.SYNOPSIS Copies selected offline Windows logs to a separate evidence directory with SHA-256.
.EXAMPLE .\Export-OfflineWindowsLogs.ps1 -WindowsPath D:\Windows -Destination E:\case\logs
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Low')]
param([Parameter(Mandatory)][string]$WindowsPath,[Parameter(Mandatory)][string]$Destination)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$sources=@('Logs\CBS\CBS.log','Logs\DISM\dism.log','Panther\setupact.log','Panther\setuperr.log','INF\setupapi.dev.log','System32\LogFiles\Srt\SrtTrail.txt')
$manifest=@()
foreach($relative in $sources){$src=Join-Path $WindowsPath $relative;if(Test-Path -LiteralPath $src){$dst=Join-Path $Destination $relative;New-Item -ItemType Directory -Path (Split-Path -Parent $dst)-Force|Out-Null;if($PSCmdlet.ShouldProcess($src,"Copy to $dst")){Copy-Item -LiteralPath $src -Destination $dst;$manifest+=[ordered]@{source=$relative;sha256=(Get-FileHash $dst -Algorithm SHA256).Hash.ToLowerInvariant()}}}}
$manifest|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $Destination 'offline-log-manifest.json') -Encoding utf8
$manifest
