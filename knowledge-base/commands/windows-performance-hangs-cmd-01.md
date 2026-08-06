# Perf counters

Karta współdzielona przez `windows-performance-hangs`. Aktualna treść:

## perf-counters

- **ID:** `windows-performance-hangs-cmd-01`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `Get-Counter '\Processor(_Total)\% Processor Time','\PhysicalDisk(_Total)\Avg. Disk sec/Transfer','\Memory\Available MBytes' -SampleInterval 2 -MaxSamples 30`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-performance-hangs/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Krótki, datowany zestaw liczników.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-wpr`, `ms-wpa`, `ms-perfmon`; zweryfikowano 2026-08-06.
