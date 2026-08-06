# Build online

Karta współdzielona przez `windows-os-identification`. Aktualna treść:

## build-online

- **ID:** `windows-os-identification-cmd-01`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `Get-ComputerInfo | Select-Object WindowsProductName,WindowsEditionId,WindowsVersion,OsBuildNumber,OsArchitecture`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-os-identification/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Jedna struktura identyfikacyjna; UBR zebrać osobno.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-win11-release`, `ms-win10-release`, `ms-lifecycle`; zweryfikowano 2026-08-06.
