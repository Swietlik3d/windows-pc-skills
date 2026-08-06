# Driver Store plan

Karta współdzielona przez `windows-drivers-devices`. Aktualna treść:

## driver-store-plan

- **ID:** `windows-drivers-devices-cmd-03`
- **Kontekst:** Windows — PowerShell jako administrator
- **Składnia:** `& '.\scripts\repair\Invoke-DriverStoreRepair.ps1' -Mode Scan -PublishedName '<OEM_INF>' -LogRoot '<CASE_LOGS>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-drivers-devices/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Plan z provider/version/dependencies bez usunięcia.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian w Scan.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-pnputil`, `ms-setupapi`, `ms-driver-store`; zweryfikowano 2026-08-06.
