# Instrukcje testów

- Testy nie mogą dotykać usług, rejestru, BCD, sieci, Defendera, driverów, partycji ani firmware.
- Używaj tylko katalogów tymczasowych, fixture i mocków. Testuj `WhatIf`/Scan oraz exit codes.
- Nie ukrywaj brakującej zależności: raportuj `SKIP` z nazwą i wymaganiem wersji.
- Nowy antywzorzec dodaj do safety lintera wraz z pozytywnym fixture dokumentacyjnym.
