# ACL odczyt

Karta współdzielona przez `windows-ntfs-permissions-shares`. Aktualna treść:

## acl-odczyt

- **ID:** `windows-ntfs-permissions-shares-cmd-01`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `Get-Acl -LiteralPath '<TARGET>' | Format-List Path,Owner,AccessToString,AreAccessRulesProtected`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-ntfs-permissions-shares/references/compatibility.md); placeholdery muszą być rozwinięte.
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
