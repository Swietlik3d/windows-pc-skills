# SetupDiag

Karta współdzielona przez `windows-setup-upgrade-rollback`. Aktualna treść:

## setupdiag

- **ID:** `windows-setup-upgrade-rollback-cmd-02`
- **Kontekst:** Windows — CMD jako administrator
- **Składnia:** `"<VERIFIED_SETUPDIAG>" /Output:<OUTPUT>\SetupDiagResults.log /Format:log`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-setup-upgrade-rollback/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Raport reguł; narzędzie musi pochodzić z Microsoft lub systemu.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Usunąć raport.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-setupdiag`, `ms-setup-logfiles`, `ms-release-health`; zweryfikowano 2026-08-06.
