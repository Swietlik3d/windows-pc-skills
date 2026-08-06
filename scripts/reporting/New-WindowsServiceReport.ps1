<#
.SYNOPSIS Generates a technical report and owner summary from case JSONL.
.EXAMPLE .\New-WindowsServiceReport.ps1 -CasePath .\cases\2026-01-01-example
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Low')]
param([Parameter(Mandatory)][string]$CasePath,[switch]$RequireValidation)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$resolved=(Resolve-Path -LiteralPath $CasePath).Path
$intake=Get-Content -LiteralPath (Join-Path $resolved 'intake.yaml') -Raw|ConvertFrom-Json
$actions=@()
Get-Content -LiteralPath (Join-Path $resolved 'actions.jsonl')|Where-Object {$_ -match '\S'}|ForEach-Object {$actions+=($_|ConvertFrom-Json)}
$validations=@($actions|Where-Object {$_.purpose -match '(?i)validat|sprawd|regress'})
if($RequireValidation -and $validations.Count -eq 0){throw 'No validation action found; report cannot be finalized.'}
$actionLines=if($actions.Count){($actions|ForEach-Object {"- $($_.timestamp_utc) [$($_.risk_class)] $($_.purpose): $($_.result); rollback: $($_.rollback)"}) -join "`n"}else{'- Brak zapisanych działań.'}
$status=if($validations.Count){'validated'}else{'open-unvalidated'}
$tech=@"
# Raport techniczny $($intake.case_id)

## Zakres
Autoryzacja: $($intake.authorization_level). Owner alias: $($intake.owner_alias).

## Działania
$actionLines

## Walidacja
Status: $status. Liczba rekordów walidacji: $($validations.Count).

## Ograniczenia
Raport nie zawiera haseł, tokenów ani BitLocker recovery keys. Fakty wymagają artefaktów.
"@
$owner=@"
# Podsumowanie dla właściciela

Sprawa $($intake.case_id) ma status **$status**. Zapisano $($actions.Count) czynności.
Przed zamknięciem upewnij się, że wykonano test objawu, przyczyny, regresji i backupu.
"@
if($PSCmdlet.ShouldProcess($resolved,'Generate reports')){$tech|Set-Content -LiteralPath (Join-Path $resolved 'technical-report.md') -Encoding utf8;$owner|Set-Content -LiteralPath (Join-Path $resolved 'owner-summary.md') -Encoding utf8}
[pscustomobject]@{Case=$intake.case_id;Actions=$actions.Count;Validations=$validations.Count;Status=$status}
