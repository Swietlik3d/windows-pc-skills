# Playbooki: Wsparcie Windows 10

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-10-support-pb-01: 22H2 po EOL

**Objaw i zakres:** Home/Pro działa po 2025-10-14.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak ESU na Internet-connected device, unsupported app/security stack, hardware not Win11 eligible, managed licensing. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- edition/channel/build.
- ESU enrollment/status.
- LTSC exact product.
- hardware eligibility.
- backup/migration blockers.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Bez ESU brak regularnych security updates.**, wykonaj tylko test: Ustalić edition i legalny ESU/enrollment lub plan migracji.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Ustalić edition i legalny ESU/enrollment lub plan migracji.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nie obiecywać wsparcia; ograniczyć exposure do migracji. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Urządzenie ma ESU z aktualnymi KB albo przeszło na supported OS. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak ESU na Internet-connected device, unsupported app/security stack, hardware not Win11 eligible, managed licensing.

## windows-10-support-pb-02: LTSC lifecycle

**Objaw i zakres:** Enterprise LTSC pozostaje w firmie.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak ESU na Internet-connected device, unsupported app/security stack, hardware not Win11 eligible, managed licensing. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- edition/channel/build.
- ESU enrollment/status.
- LTSC exact product.
- hardware eligibility.
- backup/migration blockers.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Daty różnią się między Enterprise i IoT.**, wykonaj tylko test: Porównać exact ProductName/EditionID z matrix.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Porównać exact ProductName/EditionID z matrix.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Stosować organizacyjne servicing i migration plan. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Raport podaje konkretny product lifecycle, nie ogólne „Windows 10”. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak ESU na Internet-connected device, unsupported app/security stack, hardware not Win11 eligible, managed licensing.

## windows-10-support-pb-03: PC nie spełnia Windows 11

**Objaw i zakres:** TPM/CPU blocker.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak ESU na Internet-connected device, unsupported app/security stack, hardware not Win11 eligible, managed licensing. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- edition/channel/build.
- ESU enrollment/status.
- LTSC exact product.
- hardware eligibility.
- backup/migration blockers.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Bypass obniży wspieralność.**, wykonaj tylko test: Sprawdzić oficjalne wymagania i firmware OEM.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Sprawdzić oficjalne wymagania i firmware OEM.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Rozważyć wymianę, supported Windows 10 ESU lub alternatywny supported OS; bez bypass. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Wybrana opcja ma patching, backup i datę wyjścia. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak ESU na Internet-connected device, unsupported app/security stack, hardware not Win11 eligible, managed licensing.
