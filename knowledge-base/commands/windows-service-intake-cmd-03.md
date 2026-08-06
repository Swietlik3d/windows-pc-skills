# Szablon zgody

Karta współdzielona przez `windows-service-intake`. Aktualna treść:

## szablon-zgody

- **ID:** `windows-service-intake-cmd-03`
- **Kontekst:** Repo — PowerShell 5.1+
- **Składnia:** `Copy-Item -LiteralPath '.\templates\customer-consent\authorization-pl.md' -Destination '<CASE>\authorization.md'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-service-intake/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R1`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Powstaje kopia do ręcznego uzupełnienia.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Usunąć kopię przed podpisaniem.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-bitlocker-overview`, `ms-privacy`, `codex-skills`; zweryfikowano 2026-08-06.
