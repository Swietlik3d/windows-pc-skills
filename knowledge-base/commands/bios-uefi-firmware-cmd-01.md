# Wersja firmware

Karta współdzielona przez `bios-uefi-firmware`. Aktualna treść:

## wersja-firmware

- **ID:** `bios-uefi-firmware-cmd-01`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `Get-CimInstance -ClassName Win32_BIOS | Select-Object Manufacturer,SMBIOSBIOSVersion,ReleaseDate`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/bios-uefi-firmware/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Dokładna wersja i data firmware.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-secure-boot-2026`, `ms-tpm`, `ms-bitlocker-overview`; zweryfikowano 2026-08-06.
