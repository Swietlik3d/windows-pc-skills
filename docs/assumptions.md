# Założenia

- Bieżący katalog zawierał wyłącznie master prompt i nie był repozytorium, więc repo utworzono
  bez podkatalogu.
- Oficjalny snapshot Agent Skills z 2026-08-06 wskazuje repo scope `.agents/skills`, user scope
  `$HOME/.agents/skills`, required `name`/`description` i wspierane `agents/openai.yaml`.
- Machine-readable `.yaml` używa JSON, poprawnego podzbioru YAML 1.2, aby walidacja nie wymagała
  pobierania bibliotek.
- User-wide oznacza bieżącego użytkownika, nie all-users/admin.
- Skrypty repair mogą wykonać zmiany dopiero po `-Apply`; na hoście budowy testuje się tylko Scan,
  WhatIf, fixture i parser syntax.
- Exact rolling version pozostaje `rolling`/`unknown`, jeżeli official page nie udostępnia
  stabilnego machine-readable faktu bez pobierania; nie zgadujemy.
