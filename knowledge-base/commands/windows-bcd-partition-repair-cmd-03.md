# Kontrolowana naprawa

Karta współdzielona przez `windows-bcd-partition-repair`. Aktualna treść:

## kontrolowana-naprawa

- **ID:** `windows-bcd-partition-repair-cmd-03`
- **Kontekst:** WinRE — PowerShell
- **Składnia:** `& '<REPO>\scripts\repair\Invoke-BootRepair.ps1' -Mode Plan -OsVolume '<OS_VOLUME>' -SystemVolume '<ESP_VOLUME>' -Firmware UEFI`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-bcd-partition-repair/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Plan pokazuje dokładne cele, backup i polecenia bez wykonania.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian w Mode Plan.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-bcdboot`, `ms-bcdedit`, `ms-bootrec`; zweryfikowano 2026-08-06.
