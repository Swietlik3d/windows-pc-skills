<#
.SYNOPSIS Creates an anonymized Windows service case from repository templates.
.EXAMPLE .\New-WindowsServiceCase.ps1 -Slug boot-loop -OwnerAlias owner-001 -AuthorizationLevel R0 -Root .\cases
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Low')]
param(
    [Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{1,48}$')][string]$Slug,
    [Parameter(Mandatory)][ValidatePattern('^[a-zA-Z0-9_-]{2,64}$')][string]$OwnerAlias,
    [Parameter(Mandatory)][ValidateSet('R0','R1','R2','R3','R4')][string]$AuthorizationLevel,
    [Parameter(Mandatory)][string]$Root,
    [datetime]$Date = (Get-Date)
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$module=Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1'
Import-Module $module -Force
$caseId='{0}-{1}' -f $Date.ToString('yyyy-MM-dd'),$Slug
$casePath=Join-Path ([IO.Path]::GetFullPath($Root)) $caseId
if(Test-Path -LiteralPath $casePath){throw "Case already exists: $casePath"}
if($PSCmdlet.ShouldProcess($casePath,'Create service case')){
    New-Item -ItemType Directory -Path $casePath -Force|Out-Null
    foreach($dir in @('evidence','logs','before','after')){New-Item -ItemType Directory -Path (Join-Path $casePath $dir)-Force|Out-Null}
    $intake=[ordered]@{case_id=$caseId;created_utc=[DateTime]::UtcNow.ToString('o');owner_alias=$OwnerAlias;authorization_level=$AuthorizationLevel;data_value='unknown';backup_status='unknown';encryption_status='unknown';managed_status='unknown';symptom='uncollected';last_changes=@();accessories=@()}
    Write-WmJson $intake (Join-Path $casePath 'intake.yaml')
    Copy-Item -LiteralPath (Join-Path $repo 'templates\customer-consent\authorization-pl.md') -Destination (Join-Path $casePath 'authorization.md')
    Write-WmJson ([ordered]@{status='not-collected';synthetic=$false}) (Join-Path $casePath 'inventory.json')
    Set-Content -LiteralPath (Join-Path $casePath 'symptoms.md') -Value "# Objawy`n`nNie zebrano jeszcze objawów.`n" -Encoding utf8
    Set-Content -LiteralPath (Join-Path $casePath 'timeline.jsonl') -Value '' -Encoding utf8
    Copy-Item -LiteralPath (Join-Path $repo 'templates\case\hypotheses.yaml') -Destination (Join-Path $casePath 'hypotheses.yaml')
    Set-Content -LiteralPath (Join-Path $casePath 'actions.jsonl') -Value '' -Encoding utf8
    Set-Content -LiteralPath (Join-Path $casePath 'rollback.md') -Value "# Rollback`n`nBrak zmian; uzupełnij przed R1+.`n" -Encoding utf8
    Set-Content -LiteralPath (Join-Path $casePath 'technical-report.md') -Value "# Raport techniczny`n`nStatus: open.`n" -Encoding utf8
    Set-Content -LiteralPath (Join-Path $casePath 'owner-summary.md') -Value "# Podsumowanie`n`nSprawa otwarta.`n" -Encoding utf8
}
Write-Output $casePath
