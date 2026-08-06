# ACL backup

Karta współdzielona przez `windows-ntfs-permissions-shares`. Aktualna treść:

## acl-backup

- **ID:** `windows-ntfs-permissions-shares-cmd-02`
- **Kontekst:** Windows — CMD jako administrator
- **Składnia:** `icacls "<TARGET>" /save "<BACKUP>\acl.txt" /t /c`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-ntfs-permissions-shares/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R1`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Eksport ACL; może ujawnić nazwy ścieżek, więc podlega redakcji.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** icacls <PARENT> /restore wymaga osobnego R3 gate.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-icacls`, `ms-smbshare`, `ms-efs`; zweryfikowano 2026-08-06.
