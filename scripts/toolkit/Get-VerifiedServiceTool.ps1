<#
.SYNOPSIS Resolves a catalog entry and optionally downloads an exact, verifiable asset without executing it.
.DESCRIPTION Default WhatIf is recommended. Actual download requires a direct HTTPS asset, exact version, expected SHA-256, license acceptance and ShouldProcess.
.EXAMPLE .\Get-VerifiedServiceTool.ps1 -ToolId rufus -Destination .\staging -WhatIf
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='High')]
param(
 [Parameter(Mandatory)][ValidatePattern('^[a-z0-9-]+$')][string]$ToolId,
 [Parameter(Mandatory)][string]$Destination,
 [string]$Version,
 [string]$AssetUrl,
 [ValidatePattern('^[a-fA-F0-9]{64}$')][string]$ExpectedSha256,
 [switch]$AcceptLicense
)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$catalog=Get-Content -LiteralPath (Join-Path $repo 'tools\catalog.yaml') -Raw|ConvertFrom-Json
$tool=@($catalog|Where-Object id -eq $ToolId)
if($tool.Count -ne 1){throw "Unknown/duplicate ToolId: $ToolId"}
$item=$tool[0]
$resolvedVersion=if($Version){$Version}else{$item.current_version}
$plan=[ordered]@{tool=$item.name;version=$resolvedVersion;official_home=$item.official_home;license=$item.license;commercial_use=$item.commercial_use;redistribution=$item.redistribution;signature_method=$item.signature_method;checksum_method=$item.checksum_method;asset_url=$AssetUrl;will_execute=$false}
Write-Verbose (($plan|Format-List|Out-String).Trim())
if(-not $AssetUrl){return [pscustomobject]$plan}
if($resolvedVersion -match '^(rolling|unknown|os-component|service|per-tool)'){throw 'Exact version is required before download.'}
if($AssetUrl -notmatch '^https://'){throw 'Only explicit HTTPS asset URLs are allowed.'}
if(-not $ExpectedSha256){throw 'ExpectedSha256 from an official source is required.'}
if(-not $AcceptLicense){throw "Read and accept license '$($item.license)' with -AcceptLicense."}
if(-not $PSCmdlet.ShouldProcess("$AssetUrl -> $Destination","Download $($item.name) $resolvedVersion and verify; never execute")){return [pscustomobject]$plan}
$destinationRoot=[IO.Path]::GetFullPath($Destination);New-Item -ItemType Directory -Path $destinationRoot -Force|Out-Null
$temp=Join-Path ([IO.Path]::GetTempPath()) ('wmtool-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temp -Force|Out-Null
try{
 $leaf=[IO.Path]::GetFileName(([uri]$AssetUrl).AbsolutePath);if(-not $leaf){throw 'Asset URL has no filename.'}
 $download=Join-Path $temp $leaf
 Invoke-WebRequest -Uri $AssetUrl -OutFile $download -MaximumRedirection 5 -TimeoutSec 120
 $actual=(Get-FileHash -LiteralPath $download -Algorithm SHA256).Hash.ToLowerInvariant()
 if($actual -cne $ExpectedSha256.ToLowerInvariant()){throw "SHA-256 mismatch; expected $ExpectedSha256, got $actual"}
 $signature=Get-AuthenticodeSignature -FilePath $download
 if($item.signature_method -match 'Authenticode' -and $signature.Status -ne 'Valid'){throw "Authenticode required but status is $($signature.Status)"}
 $final=Join-Path $destinationRoot $leaf;Move-Item -LiteralPath $download -Destination $final
 $provenance=[ordered]@{tool_id=$ToolId;version=$resolvedVersion;source=$AssetUrl;downloaded_utc=[DateTime]::UtcNow.ToString('o');bytes=(Get-Item $final).Length;sha256=$actual;signature_status=$signature.Status.ToString();license=$item.license;executed=$false}
 $provenance|ConvertTo-Json -Depth 8|Set-Content -LiteralPath "$final.provenance.json" -Encoding utf8
 [pscustomobject]$provenance
}finally{if(Test-Path -LiteralPath $temp){Remove-Item -LiteralPath $temp -Recurse -Force}}
