<#
.SYNOPSIS Creates a redacted Windows repair bundle from live read-only collectors or synthetic fixtures.
.DESCRIPTION Modes: Basic, Full, Offline, Network, Boot, Update, BSOD, MalwareTriage. The script never collects passwords, cookies, tokens, full product keys or BitLocker recovery keys.
.EXAMPLE .\Get-WindowsRepairBundle.ps1 -Mode Basic -FixtureRoot .\tests\fixtures\repair-bundle -OutputPath .\dist\sample-bundle
#>
[CmdletBinding()]
param(
 [Parameter(Mandatory)][ValidateSet('Basic','Full','Offline','Network','Boot','Update','BSOD','MalwareTriage')][string]$Mode,
 [string]$FixtureRoot,
 [Parameter(Mandatory)][string]$OutputPath,
 [switch]$IncludeSensitive
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$out=[IO.Path]::GetFullPath($OutputPath)
if(Test-Path -LiteralPath $out){throw "Output already exists: $out"}
New-Item -ItemType Directory -Path $out -Force|Out-Null
try{
 $records=@()
 if($FixtureRoot){
  $fixture=(Resolve-Path -LiteralPath $FixtureRoot).Path
  foreach($file in Get-ChildItem -LiteralPath $fixture -File -Recurse){
   $raw=Get-Content -LiteralPath $file.FullName -Raw
   $safe=Protect-WmText -Text $raw -IncludeSensitive:$IncludeSensitive
   $relative=Get-WmRelativePath -BasePath $fixture -Path $file.FullName
   $target=Join-Path $out $relative
   New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force|Out-Null
   Set-Content -LiteralPath $target -Value $safe -Encoding utf8
   $records+=[ordered]@{name=$relative;source='synthetic-fixture';redacted=(-not $IncludeSensitive)}
  }
  $source='fixture'
 }else{
  if($PSVersionTable.PSVersion.Major -ge 6 -and -not $IsWindows){throw 'Live collection requires Windows. Use -FixtureRoot.'}
  $os=Get-CimInstance Win32_OperatingSystem|Select-Object Caption,Version,BuildNumber,OSArchitecture,Locale
  $cs=Get-CimInstance Win32_ComputerSystem|Select-Object Manufacturer,Model,SystemType,PartOfDomain
  $bios=Get-CimInstance Win32_BIOS|Select-Object Manufacturer,SMBIOSBIOSVersion,ReleaseDate
  $data=[ordered]@{os=$os;computer=$cs;firmware=$bios;mode=$Mode;note='Live R0 only; detailed collectors should be run explicitly.'}
  $json=Protect-WmText -Text ($data|ConvertTo-Json -Depth 8) -IncludeSensitive:$IncludeSensitive
  Set-Content -LiteralPath (Join-Path $out 'basic.json') -Value $json -Encoding utf8
  $records+=[ordered]@{name='basic.json';source='live-read-only';redacted=(-not $IncludeSensitive)}
  $source='live-read-only'
 }
 $forbidden='(?i)(RecoveryPassword\s*[:=]\s*\S+|password\s*[:=]\s*\S+|token\s*[:=]\s*\S+|cookie\s*[:=]\s*\S+|\b\d{6}(?:-\d{6}){7}\b)'
 foreach($file in Get-ChildItem -LiteralPath $out -File -Recurse){
  $text=Get-Content -LiteralPath $file.FullName -Raw
  if($text -match $forbidden){throw "Secret pattern remained after redaction: $($file.Name)"}
 }
 $manifestEntries=@()
 foreach($file in Get-ChildItem -LiteralPath $out -File -Recurse|Sort-Object FullName){
   $manifestEntries+=[ordered]@{path=(Get-WmRelativePath -BasePath $out -Path $file.FullName);bytes=$file.Length;sha256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
 }
 $manifest=[ordered]@{schema_version='1.0.0';created_utc=[DateTime]::UtcNow.ToString('o');mode=$Mode;source=$source;redacted=(-not $IncludeSensitive);exclusions=@('passwords','cookies','tokens','full product keys','BitLocker recovery keys','browser contents');files=$manifestEntries}
 Write-WmJson $manifest (Join-Path $out 'manifest.json')
 $md=@"
# Windows Repair Bundle

- Mode: $Mode
- Source: $source
- Redacted: $(-not $IncludeSensitive)
- Files before manifest: $($manifestEntries.Count)
- Created UTC: $($manifest.created_utc)

Bundle is diagnostic evidence, not a diagnosis. No repair was executed.
"@
 Set-Content -LiteralPath (Join-Path $out 'summary.md') -Value $md -Encoding utf8
 $html="<html><meta charset='utf-8'><body><h1>Windows Repair Bundle</h1><p>Mode: $Mode</p><p>Source: $source</p><p>Redacted: $(-not $IncludeSensitive)</p><p>No repair executed.</p></body></html>"
 Set-Content -LiteralPath (Join-Path $out 'summary.html') -Value $html -Encoding utf8
 $zip="$out.zip"
 Compress-Archive -Path (Join-Path $out '*') -DestinationPath $zip -CompressionLevel Optimal
 $zipHash=(Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
 [pscustomobject]@{OutputPath=$out;ZipPath=$zip;ZipSha256=$zipHash;Mode=$Mode;Source=$source;Redacted=(-not $IncludeSensitive)}
 exit 0
}catch{
 [Console]::Error.WriteLine($_.Exception.Message)
 exit 30
}
