# Playbooki: Sprawa, dowody i raport zmian

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-case-evidence-pb-01: Zapis pojedynczej czynności

**Objaw i zakres:** Technik zebrał log R0.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
podejrzenie przestępstwa, brak zgody na kopiowanie danych, artefakt zawiera recovery key lub token, źródłowy nośnik ulega degradacji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- czas UTC.
- operator.
- cel czynności.
- hash SHA-256.
- źródło i kopia robocza.
- rollback.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Brak wpisu utrudni korelację i audyt.**, wykonaj tylko test: Obliczyć hash i dopisać niezmienny JSONL.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Obliczyć hash i dopisać niezmienny JSONL.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nie edytować wcześniejszych rekordów; korekty dopisywać. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Timeline jest parsowalny, a hash pliku zgodny. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
podejrzenie przestępstwa, brak zgody na kopiowanie danych, artefakt zawiera recovery key lub token, źródłowy nośnik ulega degradacji.

## windows-case-evidence-pb-02: Anonimizacja bundle

**Objaw i zakres:** Log zawiera username, hostname i e-mail.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
podejrzenie przestępstwa, brak zgody na kopiowanie danych, artefakt zawiera recovery key lub token, źródłowy nośnik ulega degradacji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- czas UTC.
- operator.
- cel czynności.
- hash SHA-256.
- źródło i kopia robocza.
- rollback.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **PII może wyciec do raportu.**, wykonaj tylko test: Pracować na kopii, zastosować deterministyczne tokeny redakcji.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Pracować na kopii, zastosować deterministyczne tokeny redakcji.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Zachować mapę tylko poza repo i za zgodą. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Test redakcji nie znajduje wzorców PII ani sekretów. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
podejrzenie przestępstwa, brak zgody na kopiowanie danych, artefakt zawiera recovery key lub token, źródłowy nośnik ulega degradacji.

## windows-case-evidence-pb-03: Raport zamknięcia

**Objaw i zakres:** Naprawa zakończona i wykonano testy.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
podejrzenie przestępstwa, brak zgody na kopiowanie danych, artefakt zawiera recovery key lub token, źródłowy nośnik ulega degradacji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- czas UTC.
- operator.
- cel czynności.
- hash SHA-256.
- źródło i kopia robocza.
- rollback.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Raport może mylić fakt z hipotezą.**, wykonaj tylko test: Złożyć actions, evidence i validation według statusu.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Złożyć actions, evidence i validation według statusu.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Wygenerować raport techniczny i krótkie owner summary. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Każde twierdzenie ma dowód lub jawne ograniczenie. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
podejrzenie przestępstwa, brak zgody na kopiowanie danych, artefakt zawiera recovery key lub token, źródłowy nośnik ulega degradacji.
