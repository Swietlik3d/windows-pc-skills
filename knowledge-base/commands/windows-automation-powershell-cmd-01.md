# Parse syntax

Karta współdzielona przez `windows-automation-powershell`. Aktualna treść:

## parse-syntax

- **ID:** `windows-automation-powershell-cmd-01`
- **Kontekst:** Repo — PowerShell 5.1+
- **Składnia:** `$errors=$null; [System.Management.Automation.Language.Parser]::ParseFile('<SCRIPT>',[ref]$null,[ref]$errors) | Out-Null; $errors`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-automation-powershell/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Pusta lista parse errors.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-powershell-shouldprocess`, `pester-docs`, `psscriptanalyzer`; zweryfikowano 2026-08-06.
