# Offline identity

Karta współdzielona przez `winpe-offline-repair`. Aktualna treść:

## offline-identity

- **ID:** `winpe-offline-repair-cmd-01`
- **Kontekst:** WinRE/WinPE — PowerShell
- **Składnia:** `& '<REPO>\scripts\offline\Get-OfflineWindowsIdentity.ps1' -WindowsPath '<OS_VOLUME>:\Windows'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/winpe-offline-repair/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Build/edition/arch z offline hive; hive jest odmontowany.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-winpe`, `ms-dism-image`, `ms-reg`; zweryfikowano 2026-08-06.
