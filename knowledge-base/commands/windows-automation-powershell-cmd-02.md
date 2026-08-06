# Repo validation

Karta współdzielona przez `windows-automation-powershell`. Aktualna treść:

## repo-validation

- **ID:** `windows-automation-powershell-cmd-02`
- **Kontekst:** Repo — PowerShell 5.1+
- **Składnia:** `& '.\scripts\repo\Test-WindowsMasterRepo.ps1' -Category Scripts`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-automation-powershell/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Syntax/safety/Pester results z jawnie oznaczonym SKIP.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian poza raportem.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-powershell-shouldprocess`, `pester-docs`, `psscriptanalyzer`; zweryfikowano 2026-08-06.
