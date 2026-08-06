Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-WmIsElevated {
    [CmdletBinding()]
    param()
    if ($PSVersionTable.PSVersion.Major -ge 6 -and -not $IsWindows) { return $false }
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-WmRelativePath {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$BasePath,
        [Parameter(Mandatory)][string]$Path
    )
    $separator = [IO.Path]::DirectorySeparatorChar.ToString()
    $baseFull = [IO.Path]::GetFullPath($BasePath)
    if (-not $baseFull.EndsWith($separator)) { $baseFull += $separator }
    $pathFull = [IO.Path]::GetFullPath($Path)
    $baseUri = New-Object -TypeName System.Uri -ArgumentList $baseFull
    $pathUri = New-Object -TypeName System.Uri -ArgumentList $pathFull
    return [Uri]::UnescapeDataString($baseUri.MakeRelativeUri($pathUri).ToString()).Replace('/', $separator)
}

function Get-WmStringSha256 {
    [CmdletBinding()]
    param([Parameter(Mandatory)][AllowEmptyString()][string]$Text)
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Text)
        return ([BitConverter]::ToString($algorithm.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $algorithm.Dispose()
    }
}

function Protect-WmText {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][AllowEmptyString()][string]$Text,
        [switch]$IncludeSensitive
    )
    if ($IncludeSensitive) { return $Text }
    $result = $Text
    $result = [regex]::Replace($result, '(?i)([a-z0-9._%+-]+)@([a-z0-9.-]+\.[a-z]{2,})', '<EMAIL_REDACTED>')
    $result = [regex]::Replace($result, '(?i)C:\\Users\\[^\\\s"]+', 'C:\Users\<USER_REDACTED>')
    $result = [regex]::Replace($result, '\b(?:\d{1,3}\.){3}\d{1,3}\b', '<IP_REDACTED>')
    $result = [regex]::Replace($result, '(?i)(RecoveryPassword|recovery key|password|token|cookie)\s*[:=]\s*\S+', '$1=<SECRET_REDACTED>')
    $result = [regex]::Replace($result, '\b\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}\b', '<BITLOCKER_KEY_REDACTED>')
    return $result
}

function Write-WmJson {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]$InputObject,
        [Parameter(Mandatory)][string]$Path,
        [int]$Depth = 12
    )
    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $InputObject | ConvertTo-Json -Depth $Depth | Set-Content -LiteralPath $Path -Encoding utf8
}

function Add-WmJsonLine {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]$InputObject,
        [Parameter(Mandatory)][string]$Path
    )
    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $line = $InputObject | ConvertTo-Json -Depth 10 -Compress
    Add-Content -LiteralPath $Path -Value $line -Encoding utf8
}

function Get-WmPendingReboot {
    [CmdletBinding()]
    param()
    $paths = @(
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending',
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
    )
    foreach ($path in $paths) {
        if (Test-Path -LiteralPath $path) { return $true }
    }
    return $false
}

function Get-WmSafetyContext {
    [CmdletBinding()]
    param([switch]$SkipLiveChecks)
    if ($SkipLiveChecks) {
        return [pscustomobject]@{
            Synthetic = $true; Elevated = $false; OS = 'fixture'; Edition = 'fixture';
            Architecture = 'fixture'; Online = $false; PendingReboot = $false;
            BitLocker = 'fixture-no-secret'; Managed = 'fixture'
        }
    }
    $os = Get-CimInstance -ClassName Win32_OperatingSystem
    $managed = 'unknown'
    try {
        $join = & "$env:SystemRoot\System32\dsregcmd.exe" /status 2>$null
        if ($join -match 'AzureAdJoined\s*:\s*YES') { $managed = 'entra' }
        elseif ($join -match 'DomainJoined\s*:\s*YES') { $managed = 'domain' }
        else { $managed = 'personal-or-unknown' }
    } catch { $managed = 'unknown' }
    $bitLocker = 'cmdlet-unavailable'
    if (Get-Command -Name Get-BitLockerVolume -ErrorAction SilentlyContinue) {
        try {
            $bitLocker = @(Get-BitLockerVolume | Select-Object MountPoint,ProtectionStatus,LockStatus,VolumeStatus)
        } catch { $bitLocker = "query-failed: $($_.Exception.Message)" }
    }
    [pscustomobject]@{
        Synthetic = $false
        Elevated = Test-WmIsElevated
        OS = $os.Caption
        Edition = $os.OperatingSystemSKU
        Architecture = $env:PROCESSOR_ARCHITECTURE
        Online = $true
        PendingReboot = Get-WmPendingReboot
        BitLocker = $bitLocker
        Managed = $managed
    }
}

function Assert-WmApplyGate {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][bool]$Apply,
        [Parameter(Mandatory)][string]$RiskClass,
        [Parameter(Mandatory)][string]$Target,
        [string]$Confirmation,
        [switch]$RequireElevated
    )
    if (-not $Apply) { return }
    if ([string]::IsNullOrWhiteSpace($Target) -or $Target -match '^<') {
        throw 'Apply gate: exact target is required.'
    }
    if ($RequireElevated -and -not (Test-WmIsElevated)) {
        throw 'Apply gate: administrator elevation is required.'
    }
    if ($RiskClass -in @('R3','R4')) {
        $expected = "CONFIRM $RiskClass $Target"
        if ($Confirmation -cne $expected) {
            throw "Apply gate: type exactly '$expected'."
        }
    }
}

function New-WmRepairPlan {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Operation,
        [Parameter(Mandatory)][string]$RiskClass,
        [Parameter(Mandatory)][string]$Target,
        [Parameter(Mandatory)][string[]]$Steps,
        [Parameter(Mandatory)][string[]]$Rollback,
        [Parameter(Mandatory)][string]$LogRoot,
        [switch]$Synthetic
    )
    if (-not (Test-Path -LiteralPath $LogRoot)) {
        New-Item -ItemType Directory -Path $LogRoot -Force | Out-Null
    }
    $record = [ordered]@{
        schema_version = '1.0.0'
        created_utc = [DateTime]::UtcNow.ToString('o')
        operation = $Operation
        risk_class = $RiskClass
        target = $Target
        mode = 'scan-plan'
        context = Get-WmSafetyContext -SkipLiveChecks:$Synthetic
        pre_change_snapshot = @('context.json', 'operator-provided backup')
        steps = $Steps
        rollback = $Rollback
        idempotency = 'Preflight is idempotent; apply step documents exceptions.'
        status = 'planned-not-applied'
    }
    Write-WmJson -InputObject $record -Path (Join-Path $LogRoot "$Operation-plan.json")
    Write-WmJson -InputObject $record.context -Path (Join-Path $LogRoot 'context.json')
    return [pscustomobject]$record
}

Export-ModuleMember -Function Test-WmIsElevated,Get-WmRelativePath,Get-WmStringSha256,Protect-WmText,Write-WmJson,Add-WmJsonLine,Get-WmPendingReboot,Get-WmSafetyContext,Assert-WmApplyGate,New-WmRepairPlan
