# Playbooki: Router główny serwisu Windows

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-master-router-pb-01: Szerokie zgłoszenie bez diagnozy

**Objaw i zakres:** Użytkownik mówi tylko „komputer nie działa”.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
zagrożenie danych, zapach spalenizny lub spuchnięta bateria, podejrzenie incydentu, BitLocker bez gotowego recovery key. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- stan uruchamiania.
- backup i wartość danych.
- szyfrowanie.
- zarządzanie organizacji.
- ostatnia zmiana.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Awaria może należeć do hardware, boot, storage albo zasilania.**, wykonaj tylko test: Zebrać pięć bramek bezpieczeństwa i sklasyfikować etap startu.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać pięć bramek bezpieczeństwa i sklasyfikować etap startu.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Przekazać do jednego skilla o najwyższym dopasowaniu; nie wykonywać naprawy w routerze. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Router zwraca jednego primary, maksymalnie trzy supporting i poziom pewności. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
zagrożenie danych, zapach spalenizny lub spuchnięta bateria, podejrzenie incydentu, BitLocker bez gotowego recovery key.

## windows-master-router-pb-02: Wiele równoczesnych objawów

**Objaw i zakres:** Wolny start, błędy aktualizacji i znikający dysk.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
zagrożenie danych, zapach spalenizny lub spuchnięta bateria, podejrzenie incydentu, BitLocker bez gotowego recovery key. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- stan uruchamiania.
- backup i wartość danych.
- szyfrowanie.
- zarządzanie organizacji.
- ostatnia zmiana.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Objawy programowe mogą być skutkiem niestabilnego storage.**, wykonaj tylko test: Nadać priorytet ryzyku danych i korelacji czasowej.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Nadać priorytet ryzyku danych i korelacji czasowej.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Najpierw storage triage; update jako skill pomocniczy dopiero po potwierdzeniu stabilności. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Pierwszy krok pozostaje R0, a dysk nie otrzymuje zapisów. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
zagrożenie danych, zapach spalenizny lub spuchnięta bateria, podejrzenie incydentu, BitLocker bez gotowego recovery key.

## windows-master-router-pb-03: Zgłoszenie firmowe i szyfrowane

**Objaw i zakres:** Laptop Entra/MDM żąda BitLocker recovery.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
zagrożenie danych, zapach spalenizny lub spuchnięta bateria, podejrzenie incydentu, BitLocker bez gotowego recovery key. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- stan uruchamiania.
- backup i wartość danych.
- szyfrowanie.
- zarządzanie organizacji.
- ostatnia zmiana.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Zmiana firmware lub polityki mogła wywołać recovery.**, wykonaj tylko test: Potwierdzić własność, MDM i dostępność klucza bez jego zapisywania.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Potwierdzić własność, MDM i dostępność klucza bez jego zapisywania.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Skierować do security/managed-client; zatrzymać R3/R4. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Odpowiedź jasno wskazuje gate organizacyjny i nie obchodzi ochrony. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
zagrożenie danych, zapach spalenizny lub spuchnięta bateria, podejrzenie incydentu, BitLocker bez gotowego recovery key.
