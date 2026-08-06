# Validation bundle

Karta współdzielona przez `windows-post-repair-validation`. Aktualna treść:

## validation-bundle

- **ID:** `windows-post-repair-validation-cmd-01`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `& '.\scripts\diagnostics\Get-WindowsRepairBundle.ps1' -Mode Basic -FixtureRoot '<FIXTURE_ROOT>' -OutputPath '<OUTPUT>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-post-repair-validation/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Before/after comparable JSON/Markdown i SHA-256.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Usunąć bundle po retencji.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-reliability`, `ms-powercfg`, `ms-release-health`; zweryfikowano 2026-08-06.
