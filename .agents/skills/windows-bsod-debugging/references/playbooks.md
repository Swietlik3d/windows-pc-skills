# Playbooki: BSOD, dumpy i WinDbg

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-bsod-debugging-pb-01: Powtarzalny driver BSOD

**Objaw i zakres:** Ten sam bugcheck pod konkretną akcją.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage/RAM errors, brak wolnego miejsca/pagefile, Verifier bez dostępu do WinRE, WHEA hardware error. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- exact bugcheck parameters.
- dump type.
- stack/module timestamps.
- symbols.
- WHEA/events.
- repro conditions.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Sterownik może naruszać pamięć, ale moduł na stosie może być ofiarą.**, wykonaj tylko test: Analizować kilka dumpów z symbolami i korelować SetupAPI/driver changes.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Analizować kilka dumpów z symbolami i korelować SetupAPI/driver changes.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Rollback/update tylko potwierdzonego drivera OEM. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Brak bugcheck w repro i brak nowych WHEA. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage/RAM errors, brak wolnego miejsca/pagefile, Verifier bez dostępu do WinRE, WHEA hardware error.

## windows-bsod-debugging-pb-02: Losowe bugchecki

**Objaw i zakres:** Kody i moduły zmieniają się.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage/RAM errors, brak wolnego miejsca/pagefile, Verifier bez dostępu do WinRE, WHEA hardware error. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- exact bugcheck parameters.
- dump type.
- stack/module timestamps.
- symbols.
- WHEA/events.
- repro conditions.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **RAM/storage/power bardziej prawdopodobne niż wiele driverów.**, wykonaj tylko test: Przerwać software repair, testować hardware i firmware stock.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Przerwać software repair, testować hardware i firmware stock.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Naprawić stabilność przed dalszym debugowaniem. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Wiele cykli testu bez błędów i spójny dump status. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage/RAM errors, brak wolnego miejsca/pagefile, Verifier bez dostępu do WinRE, WHEA hardware error.

## windows-bsod-debugging-pb-03: Driver Verifier

**Objaw i zakres:** Podejrzenie third-party driver bez dowodu.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage/RAM errors, brak wolnego miejsca/pagefile, Verifier bez dostępu do WinRE, WHEA hardware error. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- exact bugcheck parameters.
- dump type.
- stack/module timestamps.
- symbols.
- WHEA/events.
- repro conditions.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Verifier może stworzyć boot loop.**, wykonaj tylko test: Zapewnić backup, WinRE i komendę reset; wybrać tylko podejrzane non-Microsoft drivers.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zapewnić backup, WinRE i komendę reset; wybrać tylko podejrzane non-Microsoft drivers.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Włączyć na ograniczony czas wyłącznie R3 z potwierdzeniem. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Pozyskać deterministyczny dump i wyłączyć Verifier. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage/RAM errors, brak wolnego miejsca/pagefile, Verifier bez dostępu do WinRE, WHEA hardware error.
