# Eksport BCD

Karta współdzielona przez `windows-bcd-partition-repair`. Aktualna treść:

## eksport-bcd

- **ID:** `windows-bcd-partition-repair-cmd-02`
- **Kontekst:** WinRE — Command Prompt
- **Składnia:** `bcdedit /export "<BACKUP_VOLUME>:\case\before\bcd-backup"`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-bcd-partition-repair/references/compatibility.md); placeholdery muszą być rozwinięte.
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
