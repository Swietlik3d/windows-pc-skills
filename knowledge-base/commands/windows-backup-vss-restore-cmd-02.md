# Shadow copies

Karta współdzielona przez `windows-backup-vss-restore`. Aktualna treść:

## shadow-copies

- **ID:** `windows-backup-vss-restore-cmd-02`
- **Kontekst:** Windows — PowerShell jako administrator
- **Składnia:** `Get-CimInstance -ClassName Win32_ShadowCopy | Select-Object ID,InstallDate,VolumeName,DeviceObject`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-backup-vss-restore/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Inwentaryzacja bez delete.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-vss`, `ms-file-history`, `ms-windows-backup`; zweryfikowano 2026-08-06.
