# Karty poleceń: Bezpieczny nośnik serwisowy

Karty są R0 lub planem, o ile nie wskazano inaczej. Nie kopiuj polecenia bez kontekstu.

## plan-media

- **ID:** `windows-service-media-cmd-01`
- **Kontekst:** Repo — PowerShell 5.1+
- **Składnia:** `& '.\scripts\toolkit\New-ServiceMediaPlan.ps1' -ManifestPath '.\tools\manifests\service-media.yaml' -OutputPath '<OUTPUT>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Plan katalogów/pobierania bez zapisu USB.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Usunąć plan.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-adk`, `ms-winpe`, `rufus`, `ventoy`; zweryfikowano 2026-08-06.

## integrity

- **ID:** `windows-service-media-cmd-02`
- **Kontekst:** Repo — PowerShell 5.1+
- **Składnia:** `& '.\scripts\toolkit\Test-ServiceMediaIntegrity.ps1' -Root '<MEDIA_STAGING>' -ManifestPath '<PROVENANCE_JSON>'`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Hash/signature discrepancies; brak wykonania plików.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-adk`, `ms-winpe`, `rufus`, `ventoy`; zweryfikowano 2026-08-06.

## verified-download-plan

- **ID:** `windows-service-media-cmd-03`
- **Kontekst:** Repo — PowerShell 5.1+
- **Składnia:** `& '.\scripts\toolkit\Get-VerifiedServiceTool.ps1' -ToolId '<TOOL_ID>' -Destination '<STAGING>' -WhatIf`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Wyświetla version/source/license/size bez download.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian w WhatIf.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-adk`, `ms-winpe`, `rufus`, `ventoy`; zweryfikowano 2026-08-06.
