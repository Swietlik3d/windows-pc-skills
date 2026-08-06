# Karty poleceń: Sprawa, dowody i raport zmian

Karty są R0 lub planem, o ile nie wskazano inaczej. Nie kopiuj polecenia bez kontekstu.

## dodaj-akcje

- **ID:** `windows-case-evidence-cmd-01`
- **Kontekst:** Repo — PowerShell 5.1+
- **Składnia:** `& '.\scripts\reporting\Add-WindowsCaseAction.ps1' -CasePath '<CASE>' -Purpose '<CEL>' -RiskClass R0 -Result '<WYNIK>' -Rollback 'not-applicable'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Do actions.jsonl trafia jeden rekord UTC.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Dopisać rekord korekty; nie przepisywać historii.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-get-filehash`, `nist-chain-evidence`, `ms-privacy`; zweryfikowano 2026-08-06.

## raport

- **ID:** `windows-case-evidence-cmd-02`
- **Kontekst:** Repo — PowerShell 5.1+
- **Składnia:** `& '.\scripts\reporting\New-WindowsServiceReport.ps1' -CasePath '<CASE>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Powstają technical-report.md i owner-summary.md.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Przywrócić poprzednie raporty z before/ lub historii Git.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-get-filehash`, `nist-chain-evidence`, `ms-privacy`; zweryfikowano 2026-08-06.

## hash-dowodu

- **ID:** `windows-case-evidence-cmd-03`
- **Kontekst:** Windows — PowerShell 5.1
- **Składnia:** `Get-FileHash -LiteralPath '<ARTIFACT>' -Algorithm SHA256`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Zwrócony jest 64-znakowy hash SHA-256.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-get-filehash`, `nist-chain-evidence`, `ms-privacy`; zweryfikowano 2026-08-06.
