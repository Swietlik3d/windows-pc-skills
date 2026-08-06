# BCD read Vista–8.1

Karta współdzielona przez `windows-legacy-xp-vista-7-8`. Aktualna treść:

## bcd-read-vista-8-1

- **ID:** `windows-legacy-xp-vista-7-8-cmd-03`
- **Kontekst:** WinRE — Command Prompt
- **Składnia:** `bcdedit /enum all`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-legacy-xp-vista-7-8/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Store entries bez zmiany.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-xp-lifecycle`, `ms-win7-lifecycle`, `ms-win81-lifecycle`; zweryfikowano 2026-08-06.
