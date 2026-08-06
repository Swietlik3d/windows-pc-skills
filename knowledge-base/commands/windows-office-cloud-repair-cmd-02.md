# Outlook data

Karta współdzielona przez `windows-office-cloud-repair`. Aktualna treść:

## outlook-data

- **ID:** `windows-office-cloud-repair-cmd-02`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `Get-ChildItem -LiteralPath '<OUTLOOK_DATA_ROOT>' -File -Filter '*.pst' | Select-Object FullName,Length,LastWriteTime`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-office-cloud-repair/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Inwentaryzacja PST; ścieżki redagować.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-office-repair`, `ms-onedrive`, `ms-teams-troubleshoot`; zweryfikowano 2026-08-06.
