# Playbooki: Przyjęcie urządzenia i autoryzacja

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-service-intake-pb-01: Standardowe przyjęcie

**Objaw i zakres:** Urządzenie prywatne, Windows uruchamia się.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak upoważnienia, dane krytyczne bez kopii, urządzenie firmowe bez kontaktu do administratora, oznaki cieczy lub baterii. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- tożsamość urządzenia bez sekretów.
- zakres zgody R0–R4.
- wartość i lokalizacja danych.
- stan BitLocker.
- akcesoria i stan fizyczny.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Zakres może być ustalony bez dostępu do treści prywatnych.**, wykonaj tylko test: Wypełnić intake i zgodę, zanotować stan oraz plombowanie.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Wypełnić intake i zgodę, zanotować stan oraz plombowanie.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Zezwolić na R0; kolejne klasy wymagają osobnych bramek. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Intake ma komplet wymaganych pól i podpis/znacznik zgody. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak upoważnienia, dane krytyczne bez kopii, urządzenie firmowe bez kontaktu do administratora, oznaki cieczy lub baterii.

## windows-service-intake-pb-02: Dane cenniejsze niż urządzenie

**Objaw i zakres:** Brak backupu i niestabilny dysk.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak upoważnienia, dane krytyczne bez kopii, urządzenie firmowe bez kontaktu do administratora, oznaki cieczy lub baterii. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- tożsamość urządzenia bez sekretów.
- zakres zgody R0–R4.
- wartość i lokalizacja danych.
- stan BitLocker.
- akcesoria i stan fizyczny.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Dalsze uruchamianie może zwiększać utratę.**, wykonaj tylko test: Zatrzymać testy zapisu i uzgodnić imaging/pro recovery.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zatrzymać testy zapisu i uzgodnić imaging/pro recovery.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nadać priorytet odzyskowi, nie naprawie Windows. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Zakres wyraźnie rozdziela odzysk danych od naprawy. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak upoważnienia, dane krytyczne bez kopii, urządzenie firmowe bez kontaktu do administratora, oznaki cieczy lub baterii.

## windows-service-intake-pb-03: Laptop zarządzany

**Objaw i zakres:** Entra/MDM, klient nie zna polityk.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak upoważnienia, dane krytyczne bez kopii, urządzenie firmowe bez kontaktu do administratora, oznaki cieczy lub baterii. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- tożsamość urządzenia bez sekretów.
- zakres zgody R0–R4.
- wartość i lokalizacja danych.
- stan BitLocker.
- akcesoria i stan fizyczny.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Serwis lokalny może naruszyć politykę organizacji.**, wykonaj tylko test: Zebrać tylko status zarządzania i kontakt administratora.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać tylko status zarządzania i kontakt administratora.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Ograniczyć się do R0 do czasu pisemnej zgody organizacji. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Dokumentacja wskazuje właściciela decyzji i brak obejść. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak upoważnienia, dane krytyczne bez kopii, urządzenie firmowe bez kontaktu do administratora, oznaki cieczy lub baterii.
