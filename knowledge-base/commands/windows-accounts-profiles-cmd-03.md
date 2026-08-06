# Repair plan

Karta współdzielona przez `windows-accounts-profiles`. Aktualna treść:

## repair-plan

- **ID:** `windows-accounts-profiles-cmd-03`
- **Kontekst:** Windows — PowerShell jako administrator
- **Składnia:** `& '.\scripts\repair\Invoke-UserProfileRepair.ps1' -Mode Scan -ProfilePath '<PROFILE>' -LogRoot '<CASE_LOGS>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-accounts-profiles/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Preflight EFS/OneDrive/ACL i plan bez zmian.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian w Scan.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-account-recovery`, `ms-hello`, `ms-user-profile`; zweryfikowano 2026-08-06.
