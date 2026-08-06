# Ryzyko storage

Karta współdzielona przez `storage-triage-cloning-recovery`. Aktualna treść:

## ryzyko-storage

- **ID:** `storage-triage-cloning-recovery-cmd-01`
- **Kontekst:** Windows — PowerShell jako administrator
- **Składnia:** `& '.\scripts\diagnostics\Get-WindowsStorageRisk.ps1' -FixturePath '<FIXTURE_JSON>' -OutputPath '<OUTPUT_JSON>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/storage-triage-cloning-recovery/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Klasyfikacja safe/caution/stop z dowodami.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian źródła.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `smartmontools`, `gddrescue`, `opensuperclone`, `testdisk`; zweryfikowano 2026-08-06.
