# Boot.ini read

Karta współdzielona przez `windows-legacy-xp-vista-7-8`. Aktualna treść:

## boot-ini-read

- **ID:** `windows-legacy-xp-vista-7-8-cmd-02`
- **Kontekst:** Recovery Console/WinPE — CMD
- **Składnia:** `type <SYSTEM_VOLUME>:\boot.ini`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-legacy-xp-vista-7-8/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Konfiguracja ARC paths bez edycji.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-xp-lifecycle`, `ms-win7-lifecycle`, `ms-win81-lifecycle`; zweryfikowano 2026-08-06.
