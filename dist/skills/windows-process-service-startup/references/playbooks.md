# Playbooki: Procesy, usługi i autostart

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-process-service-startup-pb-01: Usługa nie startuje

**Objaw i zakres:** Service timeout/dependency error.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
usługa bezpieczeństwa/backup/MDM, nieznany binary signature, podejrzenie malware, brak exportu konfiguracji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- process path/signature.
- service config/dependencies.
- task XML.
- startup registry.
- boot/logon timeline.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Dependency, account, binary path lub policy.**, wykonaj tylko test: Zebrać sc qc, dependencies i eventy bez start/stop.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać sc qc, dependencies i eventy bez start/stop.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Naprawić jeden parametr po eksporcie konfiguracji. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Service osiąga Running i funkcja biznesowa działa po reboot. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
usługa bezpieczeństwa/backup/MDM, nieznany binary signature, podejrzenie malware, brak exportu konfiguracji.

## windows-process-service-startup-pb-02: Wolny startup

**Objaw i zakres:** Dużo programów po logowaniu.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
usługa bezpieczeństwa/backup/MDM, nieznany binary signature, podejrzenie malware, brak exportu konfiguracji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- process path/signature.
- service config/dependencies.
- task XML.
- startup registry.
- boot/logon timeline.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Jedna lub kilka pozycji blokuje shell.**, wykonaj tylko test: Autoruns export i pomiar baseline; nie wyłączać Microsoft entries.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Autoruns export i pomiar baseline; nie wyłączać Microsoft entries.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Wyłączać po jednej pozycji z dokumentowanym rollback. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Startup krótszy, a aplikacje wymagane pozostają dostępne. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
usługa bezpieczeństwa/backup/MDM, nieznany binary signature, podejrzenie malware, brak exportu konfiguracji.

## windows-process-service-startup-pb-03: Podejrzane zadanie

**Objaw i zakres:** Losowy task uruchamia skrypt.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
usługa bezpieczeństwa/backup/MDM, nieznany binary signature, podejrzenie malware, brak exportu konfiguracji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- process path/signature.
- service config/dependencies.
- task XML.
- startup registry.
- boot/logon timeline.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Może być legalnym updaterem lub persistence.**, wykonaj tylko test: Wyeksportować XML, podpis/hash targetu i parent provenance.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Wyeksportować XML, podpis/hash targetu i parent provenance.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Przy malware przejść do incident playbook; nie kasować dowodu. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Task sklasyfikowany, dowody zachowane, brak nieautoryzowanego uruchomienia. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
usługa bezpieczeństwa/backup/MDM, nieznany binary signature, podejrzenie malware, brak exportu konfiguracji.
