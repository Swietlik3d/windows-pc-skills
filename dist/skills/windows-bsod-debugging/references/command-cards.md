# Karty poleceń: BSOD, dumpy i WinDbg

Karty są R0 lub planem, o ile nie wskazano inaczej. Nie kopiuj polecenia bez kontekstu.

## metadata-dumpa

- **ID:** `windows-bsod-debugging-cmd-01`
- **Kontekst:** Repo — PowerShell 5.1+
- **Składnia:** `& '.\scripts\diagnostics\Get-MinidumpMetadata.ps1' -Path '<MINIDUMP_FIXTURE>' -OutputPath '<OUTPUT_JSON>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Rozmiar, czas, signature i jawna informacja, że to nie pełna analiza.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-windbg`, `ms-bugcheck`, `ms-driver-verifier`; zweryfikowano 2026-08-06.

## windbg

- **ID:** `windows-bsod-debugging-cmd-02`
- **Kontekst:** Windows — WinDbg Command
- **Składnia:** `!analyze -v`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Bugcheck, parametry i stack przy poprawnych symbolach.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian w dumpie.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-windbg`, `ms-bugcheck`, `ms-driver-verifier`; zweryfikowano 2026-08-06.

## verifier-status

- **ID:** `windows-bsod-debugging-cmd-03`
- **Kontekst:** Windows — CMD jako administrator
- **Składnia:** `verifier /querysettings`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Aktualne ustawienia bez ich zmiany.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-windbg`, `ms-bugcheck`, `ms-driver-verifier`; zweryfikowano 2026-08-06.
