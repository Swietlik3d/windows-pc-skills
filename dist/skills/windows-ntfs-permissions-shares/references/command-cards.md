# Karty poleceń: NTFS ACL i udziały SMB

Karty są R0 lub planem, o ile nie wskazano inaczej. Nie kopiuj polecenia bez kontekstu.

## acl-odczyt

- **ID:** `windows-ntfs-permissions-shares-cmd-01`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `Get-Acl -LiteralPath '<TARGET>' | Format-List Path,Owner,AccessToString,AreAccessRulesProtected`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Owner i ACE bez zmian.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-icacls`, `ms-smbshare`, `ms-efs`; zweryfikowano 2026-08-06.

## acl-backup

- **ID:** `windows-ntfs-permissions-shares-cmd-02`
- **Kontekst:** Windows — CMD jako administrator
- **Składnia:** `icacls "<TARGET>" /save "<BACKUP>\acl.txt" /t /c`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
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

## share-acl

- **ID:** `windows-ntfs-permissions-shares-cmd-03`
- **Kontekst:** Windows — PowerShell jako administrator
- **Składnia:** `Get-SmbShareAccess -Name '<SHARE>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Share permissions dla principal.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-icacls`, `ms-smbshare`, `ms-efs`; zweryfikowano 2026-08-06.
