Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# These small read-only boundaries keep host APIs mockable. They do not change
# registry, services, BCD, servicing state, network state or files.
function Get-WmRegistrySnapshot {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$LiteralPath)
    Get-ItemProperty -LiteralPath $LiteralPath -ErrorAction Stop
}

function Get-WmServiceSnapshot {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$Name)
    Get-Service -Name $Name -ErrorAction Stop
}

function Get-WmBcdSnapshot {
    [CmdletBinding()]
    param()
    @(& bcdedit.exe /enum all 2>&1 | ForEach-Object { [string]$_ })
}

function Get-WmDismScanHealth {
    [CmdletBinding()]
    param()
    @(& dism.exe /Online /Cleanup-Image /ScanHealth 2>&1 | ForEach-Object { [string]$_ })
}

function Get-WmCimSnapshot {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$ClassName)
    Get-CimInstance -ClassName $ClassName -ErrorAction Stop
}

function Get-WmNetworkSnapshotBoundary {
    [CmdletBinding()]
    param()
    Get-NetIPConfiguration -ErrorAction Stop
}

function Get-WmFileSnapshot {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$LiteralPath)
    @(Get-Content -LiteralPath $LiteralPath -ErrorAction Stop) -join [Environment]::NewLine
}

Export-ModuleMember -Function Get-WmRegistrySnapshot,Get-WmServiceSnapshot,Get-WmBcdSnapshot,Get-WmDismScanHealth,Get-WmCimSnapshot,Get-WmNetworkSnapshotBoundary,Get-WmFileSnapshot
