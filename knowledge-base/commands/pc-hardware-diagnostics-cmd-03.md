# Raport zasilania

Karta współdzielona przez `pc-hardware-diagnostics`. Aktualna treść:

## raport-zasilania

- **ID:** `pc-hardware-diagnostics-cmd-03`
- **Kontekst:** Windows — CMD jako administrator
- **Składnia:** `powercfg /batteryreport /output "<OUTPUT>\battery-report.html"`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/pc-hardware-diagnostics/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Powstaje lokalny raport HTML.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Usunąć raport; nie zmienia konfiguracji.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-wmi-computersystem`, `ms-powercfg`, `ifixit-esd`; zweryfikowano 2026-08-06.
