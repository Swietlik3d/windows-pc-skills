# Layout dysków

Karta współdzielona przez `storage-triage-cloning-recovery`. Aktualna treść:

## layout-dyskow

- **ID:** `storage-triage-cloning-recovery-cmd-02`
- **Kontekst:** Windows — PowerShell jako administrator
- **Składnia:** `Get-Disk | Select-Object Number,FriendlyName,SerialNumber,PartitionStyle,OperationalStatus,HealthStatus,Size`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/storage-triage-cloning-recovery/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Jednoznaczna lista dysków; serial zanonimizować w raporcie.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `smartmontools`, `gddrescue`, `opensuperclone`, `testdisk`; zweryfikowano 2026-08-06.
