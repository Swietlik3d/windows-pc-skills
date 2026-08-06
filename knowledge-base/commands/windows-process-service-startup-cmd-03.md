# Startup

Karta współdzielona przez `windows-process-service-startup`. Aktualna treść:

## startup

- **ID:** `windows-process-service-startup-cmd-03`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `Get-CimInstance -ClassName Win32_StartupCommand | Select-Object Name,Command,Location,User`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-process-service-startup/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Widoczne klasyczne startup entries bez wymuszania MSI consistency.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-services`, `ms-scheduledtasks`, `sysinternals-autoruns`; zweryfikowano 2026-08-06.
