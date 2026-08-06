# Karty poleceń: Windows Update i servicing

Karty są R0 lub planem, o ile nie wskazano inaczej. Nie kopiuj polecenia bez kontekstu.

## update-health

- **ID:** `windows-update-servicing-cmd-01`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `& '.\scripts\diagnostics\Get-WindowsUpdateHealth.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** JSON z historią, pending i event summary.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-wu-troubleshoot`, `ms-windowsupdate-log`, `ms-release-health`; zweryfikowano 2026-08-06.

## windows-update-log

- **ID:** `windows-update-servicing-cmd-02`
- **Kontekst:** Windows — PowerShell jako administrator
- **Składnia:** `Get-WindowsUpdateLog -LogPath '<OUTPUT>\WindowsUpdate.log'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Czytelny log utworzony z ETL.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Usunąć wygenerowany log.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-wu-troubleshoot`, `ms-windowsupdate-log`, `ms-release-health`; zweryfikowano 2026-08-06.

## plan-resetu

- **ID:** `windows-update-servicing-cmd-03`
- **Kontekst:** Windows — PowerShell jako administrator
- **Składnia:** `& '.\scripts\repair\Invoke-WindowsUpdateRepair.ps1' -Mode Scan -LogRoot '<CASE_LOGS>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Plan i preflight bez zatrzymania usług/cache reset.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian w Scan.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-wu-troubleshoot`, `ms-windowsupdate-log`, `ms-release-health`; zweryfikowano 2026-08-06.
