# Mapa symptomów

Karta współdzielona przez `windows-master-router`. Aktualna treść:

## mapa-symptomow

- **ID:** `windows-master-router-cmd-02`
- **Kontekst:** Repo — Python 3
- **Składnia:** `python .\scripts\repo\route_issue.py --text "<OPIS>" --json`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-master-router/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** JSON zawiera primary, supporting, confidence i safety_flags.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian; zachować wejście tylko za zgodą.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `codex-skills`, `ms-support-troubleshoot`, `ms-bitlocker-overview`; zweryfikowano 2026-08-06.
