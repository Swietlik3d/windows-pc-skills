# Playbooki: Diagnostyka sprzętu PC

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## pc-hardware-diagnostics-pb-01: Brak reakcji na power

**Objaw i zakres:** Zero LED i wentylatorów.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
spuchnięta bateria, zapach spalenizny, ślady cieczy, iskrzenie, niepewny pinout zasilacza. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- dokładny model.
- sekwencja LED/beep.
- napięcie znamionowe zasilacza.
- minimalna konfiguracja.
- znane dobre części.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Zasilanie wejściowe, przycisk, PSU lub zwarcie płyty.**, wykonaj tylko test: Odłączyć zasilanie, ocenić wizualnie, potem testować znanym dobrym zasilaczem o zgodnej specyfikacji.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Odłączyć zasilanie, ocenić wizualnie, potem testować znanym dobrym zasilaczem o zgodnej specyfikacji.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Wymieniać jedną część naraz; żadnego otwierania PSU. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Urządzenie przechodzi powtarzalny power-on bez zapachu i nadmiernego poboru. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
spuchnięta bateria, zapach spalenizny, ślady cieczy, iskrzenie, niepewny pinout zasilacza.

## pc-hardware-diagnostics-pb-02: Zasilanie jest, brak POST

**Objaw i zakres:** Wentylatory ruszają, brak obrazu i kod.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
spuchnięta bateria, zapach spalenizny, ślady cieczy, iskrzenie, niepewny pinout zasilacza. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- dokładny model.
- sekwencja LED/beep.
- napięcie znamionowe zasilacza.
- minimalna konfiguracja.
- znane dobre części.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **RAM, GPU, CPU/IMC, firmware albo płyta.**, wykonaj tylko test: Udokumentować kod producenta, minimalizować konfigurację i testować pojedynczy moduł RAM.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Udokumentować kod producenta, minimalizować konfigurację i testować pojedynczy moduł RAM.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Reset CMOS tylko R3 po BitLocker/ustawieniach i dokumentacji. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

POST jest stabilny w trzech zimnych startach. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
spuchnięta bateria, zapach spalenizny, ślady cieczy, iskrzenie, niepewny pinout zasilacza.

## pc-hardware-diagnostics-pb-03: Laptop nie ładuje

**Objaw i zakres:** Działa z baterii, nie przyjmuje zasilania USB-C.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
spuchnięta bateria, zapach spalenizny, ślady cieczy, iskrzenie, niepewny pinout zasilacza. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- dokładny model.
- sekwencja LED/beep.
- napięcie znamionowe zasilacza.
- minimalna konfiguracja.
- znane dobre części.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Ładowarka, kabel E-marker, port, PD profile lub bateria.**, wykonaj tylko test: Porównać moc/specyfikację i użyć USB power metera bez rozbierania zasilacza.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Porównać moc/specyfikację i użyć USB power metera bez rozbierania zasilacza.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Wymienić kabel/ładowarkę na zgodne, potem port/dock jako moduł. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Ładowanie utrzymuje właściwą moc i nie przerywa pod lekkim obciążeniem. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
spuchnięta bateria, zapach spalenizny, ślady cieczy, iskrzenie, niepewny pinout zasilacza.
