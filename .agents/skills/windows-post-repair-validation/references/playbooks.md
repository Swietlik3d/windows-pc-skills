# Playbooki: Walidacja po naprawie

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-post-repair-validation-pb-01: Walidacja naprawy software

**Objaw i zakres:** Objaw już nie występuje.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
niewyjaśnione storage/RAM errors, temperatury przy limicie, backup niezweryfikowany, ochrona wyłączona, test ryzykowny dla danych. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- baseline before.
- success criteria.
- cause reproduction.
- symptom test.
- regression set.
- residual risk.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Jedna udana próba może być przypadkiem.**, wykonaj tylko test: Powtórzyć exact repro, potem reboot/sleep/user workflow.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Powtórzyć exact repro, potem reboot/sleep/user workflow.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Jeśli odchylenie wraca, cofnąć zmianę i wrócić do hipotez. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Co najmniej trzy próby lub uzasadniony okres bez regresji. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
niewyjaśnione storage/RAM errors, temperatury przy limicie, backup niezweryfikowany, ochrona wyłączona, test ryzykowny dla danych.

## windows-post-repair-validation-pb-02: Burn-in po hardware

**Objaw i zakres:** Wymieniono RAM/SSD/cooling.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
niewyjaśnione storage/RAM errors, temperatury przy limicie, backup niezweryfikowany, ochrona wyłączona, test ryzykowny dla danych. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- baseline before.
- success criteria.
- cause reproduction.
- symptom test.
- regression set.
- residual risk.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Intermittent fault może ujawnić się pod temperaturą/cyklem.**, wykonaj tylko test: Test właściwy komponentowi z limitami temperatur i stop conditions.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Test właściwy komponentowi z limitami temperatur i stop conditions.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nie wykonywać stress przy danych bez backupu. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Zero error, stabilne temperatury i cold boot/sleep cycles. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
niewyjaśnione storage/RAM errors, temperatury przy limicie, backup niezweryfikowany, ochrona wyłączona, test ryzykowny dla danych.

## windows-post-repair-validation-pb-03: Zamknięcie z ryzykiem resztkowym

**Objaw i zakres:** Nie wszystkie hipotezy można wykluczyć.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
niewyjaśnione storage/RAM errors, temperatury przy limicie, backup niezweryfikowany, ochrona wyłączona, test ryzykowny dla danych. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- baseline before.
- success criteria.
- cause reproduction.
- symptom test.
- regression set.
- residual risk.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Brak lab/long test.**, wykonaj tylko test: Wymienić wykonane dowody, limity i monitoring.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Wymienić wykonane dowody, limity i monitoring.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nie oznaczać „naprawiono” bez warunku sukcesu. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Raport rozróżnia fixed/mitigated/unverified i daje plan nawrotu. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
niewyjaśnione storage/RAM errors, temperatury przy limicie, backup niezweryfikowany, ochrona wyłączona, test ryzykowny dla danych.
