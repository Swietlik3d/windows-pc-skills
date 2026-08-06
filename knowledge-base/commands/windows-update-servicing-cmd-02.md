# Windows Update log

Karta współdzielona przez `windows-update-servicing`. Aktualna treść:

## windows-update-log

- **ID:** `windows-update-servicing-cmd-02`
- **Kontekst:** Windows — PowerShell jako administrator
- **Składnia:** `Get-WindowsUpdateLog -LogPath '<OUTPUT>\WindowsUpdate.log'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-update-servicing/references/compatibility.md); placeholdery muszą być rozwinięte.
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
