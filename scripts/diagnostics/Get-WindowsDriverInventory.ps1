<#
.SYNOPSIS Collects a redacted, read-only Windows diagnostic view or parses a synthetic JSON fixture.
.EXAMPLE .\Get-WindowsDriverInventory.ps1 -FixturePath .\tests\fixtures\sample.json -OutputPath .\dist\output.json
#>
[CmdletBinding()]
param(
    [string]$FixturePath,
    [Parameter(Mandatory)][string]$OutputPath,
    [switch]$IncludeSensitive
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
try{
    if($FixturePath){
        $resolved=(Resolve-Path -LiteralPath $FixturePath).Path
        $raw=Get-Content -LiteralPath $resolved -Raw
        try{$data=$raw|ConvertFrom-Json}catch{$data=[ordered]@{fixture_text=$raw}}
        $source='fixture'
    }else{
        if($PSVersionTable.PSVersion.Major -ge 6 -and -not $IsWindows){throw 'Live collection requires Windows. Use -FixturePath.'}
        $data=[ordered]@{
            collected_utc=[DateTime]::UtcNow.ToString('o')
            drivers=@(Get-CimInstance -ClassName Win32_PnPSignedDriver|Select-Object DeviceName,DeviceID,DriverProviderName,DriverVersion,DriverDate,InfName,IsSigned)
            problem_devices=@(Get-CimInstance -ClassName Win32_PnPEntity|Where-Object ConfigManagerErrorCode -ne 0|Select-Object Name,PNPDeviceID,ConfigManagerErrorCode,Status)
        }
        $source='live-read-only'
    }
    $json=$data|ConvertTo-Json -Depth 12
    $protected=Protect-WmText -Text $json -IncludeSensitive:$IncludeSensitive
    $envelope=[ordered]@{schema_version='1.0.0';collector='Get-WindowsDriverInventory.ps1';source=$source;collected_utc=[DateTime]::UtcNow.ToString('o');redacted=(-not $IncludeSensitive);data=($protected|ConvertFrom-Json)}
    Write-WmJson -InputObject $envelope -Path $OutputPath
    $envelope
    exit 0
}catch{
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 20
}
