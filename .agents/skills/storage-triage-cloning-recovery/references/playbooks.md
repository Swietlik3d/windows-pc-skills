# Playbooki: Storage triage, klonowanie i odzysk

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## storage-triage-cloning-recovery-pb-01: Klikający HDD

**Objaw i zakres:** Dysk wydaje dźwięki i zwalnia.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
klikający lub znikający dysk, rosnące read errors, critical warning NVMe, źródło/cel nie są jednoznaczne. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- model/serial z redakcją.
- SMART/NVMe health.
- read error trend.
- wartość danych.
- write blocker.
- mapfile imaging.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Uszkodzenie mechaniczne, każda próba może pogorszyć stan.**, wykonaj tylko test: Wyłączyć, nie skanować powierzchni, uzgodnić profesjonalne odzyskiwanie.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Wyłączyć, nie skanować powierzchni, uzgodnić profesjonalne odzyskiwanie.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Imaging tylko jeśli zaakceptowano ryzyko i nośnik stabilny; preferować hardware imager. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Sukces oznacza zachowany obraz/hash, nie „naprawiony” dysk. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
klikający lub znikający dysk, rosnące read errors, critical warning NVMe, źródło/cel nie są jednoznaczne.

## storage-triage-cloning-recovery-pb-02: SSD/NVMe znika

**Objaw i zakres:** Dysk okresowo znika z UEFI.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
klikający lub znikający dysk, rosnące read errors, critical warning NVMe, źródło/cel nie są jednoznaczne. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- model/serial z redakcją.
- SMART/NVMe health.
- read error trend.
- wartość danych.
- write blocker.
- mapfile imaging.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Firmware, zasilanie, temperatura albo kontroler NAND.**, wykonaj tylko test: Korelować SMART/NVMe, temperaturę i obecność w UEFI bez zapisów.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Korelować SMART/NVMe, temperaturę i obecność w UEFI bez zapisów.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Najpierw imaging na inny nośnik; firmware dopiero po kopii i OEM gate. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Źródłowy dysk nie jest ponownie używany jako jedyna kopia. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
klikający lub znikający dysk, rosnące read errors, critical warning NVMe, źródło/cel nie są jednoznaczne.

## storage-triage-cloning-recovery-pb-03: Odzysk logiczny po usunięciu

**Objaw i zakres:** Pliki skasowane, dysk stabilny.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
klikający lub znikający dysk, rosnące read errors, critical warning NVMe, źródło/cel nie są jednoznaczne. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- model/serial z redakcją.
- SMART/NVMe health.
- read error trend.
- wartość danych.
- write blocker.
- mapfile imaging.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **TRIM mógł wyzerować bloki na SSD.**, wykonaj tylko test: Natychmiast zatrzymać zapisy i utworzyć obraz read-only.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Natychmiast zatrzymać zapisy i utworzyć obraz read-only.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Analizować kopię TestDisk/PhotoRec/DMDE; wyniki zapisywać na trzeci nośnik. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Otworzyć reprezentatywną próbkę i zachować log narzędzia. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
klikający lub znikający dysk, rosnące read errors, critical warning NVMe, źródło/cel nie są jednoznaczne.
