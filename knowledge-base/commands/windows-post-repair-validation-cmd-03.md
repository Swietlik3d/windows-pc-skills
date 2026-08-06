# Event regression

Karta współdzielona przez `windows-post-repair-validation`. Aktualna treść:

## event-regression

- **ID:** `windows-post-repair-validation-cmd-03`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `Get-WinEvent -FilterHashtable @{LogName='System';StartTime='<REPAIR_COMPLETED_UTC>'} | Where-Object LevelDisplayName -in 'Critical','Error'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-post-repair-validation/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Nowe krytyczne/błędy do korelacji, nie automatyczna diagnoza.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-reliability`, `ms-powercfg`, `ms-release-health`; zweryfikowano 2026-08-06.
