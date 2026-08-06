# Activation UI

Karta współdzielona przez `windows-activation-licensing`. Aktualna treść:

## activation-ui

- **ID:** `windows-activation-licensing-cmd-03`
- **Kontekst:** Windows — interfejs PL/EN/NL
- **Składnia:** `Ustawienia / Settings / Instellingen → System → Aktywacja / Activation / Activering`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-activation-licensing/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Widoczny status i oficjalny troubleshooter.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian do momentu świadomego kliknięcia.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-activation`, `ms-activation-troubleshooter`, `ms-volume-activation`; zweryfikowano 2026-08-06.
