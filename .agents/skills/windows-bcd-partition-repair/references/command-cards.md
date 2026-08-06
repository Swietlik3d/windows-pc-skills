# Karty poleceń: BCD, ESP i partycje startowe

Karty są R0 lub planem, o ile nie wskazano inaczej. Nie kopiuj polecenia bez kontekstu.

## plan-layoutu

- **ID:** `windows-bcd-partition-repair-cmd-01`
- **Kontekst:** WinRE — PowerShell
- **Składnia:** `& '<REPO>\scripts\diagnostics\Get-WindowsBootLayout.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Jednoznaczna mapa dysk→partycja→rola.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-bcdboot`, `ms-bcdedit`, `ms-bootrec`; zweryfikowano 2026-08-06.

## eksport-bcd

- **ID:** `windows-bcd-partition-repair-cmd-02`
- **Kontekst:** WinRE — Command Prompt
- **Składnia:** `bcdedit /export "<BACKUP_VOLUME>:\case\before\bcd-backup"`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R1`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Powstaje kopia store; katalog docelowy jest poza źródłowym ESP.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** bcdedit /import wymaga osobnego R3 gate.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-bcdboot`, `ms-bcdedit`, `ms-bootrec`; zweryfikowano 2026-08-06.

## kontrolowana-naprawa

- **ID:** `windows-bcd-partition-repair-cmd-03`
- **Kontekst:** WinRE — PowerShell
- **Składnia:** `& '<REPO>\scripts\repair\Invoke-BootRepair.ps1' -Mode Plan -OsVolume '<OS_VOLUME>' -SystemVolume '<ESP_VOLUME>' -Firmware UEFI`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
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
