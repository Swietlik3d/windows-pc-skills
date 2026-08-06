# Playbooki: Peryferia Windows

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-peripherals-repair-pb-01: Kolejka drukarki stoi

**Objaw i zakres:** Jobs pozostają w queue.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
przegrzewający się port/kabel, uszkodzenie mechaniczne, managed print policy, kamera/mikrofon z policy privacy. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- problem device IDs.
- port/cable/dock path.
- driver and firmware.
- service/event logs.
- privacy policy.
- known-good peripheral.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Spooler job/driver/port może być uszkodzony.**, wykonaj tylko test: Wyeksportować queue, driver i PrintService events.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Wyeksportować queue, driver i PrintService events.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Usunąć tylko wskazany job lub kontrolowanie wyczyścić spool po backupie. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Test page i realny dokument drukują po reboot. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
przegrzewający się port/kabel, uszkodzenie mechaniczne, managed print policy, kamera/mikrofon z policy privacy.

## windows-peripherals-repair-pb-02: Brak audio

**Objaw i zakres:** Output device istnieje, brak dźwięku.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
przegrzewający się port/kabel, uszkodzenie mechaniczne, managed print policy, kamera/mikrofon z policy privacy. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- problem device IDs.
- port/cable/dock path.
- driver and firmware.
- service/event logs.
- privacy policy.
- known-good peripheral.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Endpoint selection, service, driver, privacy lub dock.**, wykonaj tylko test: Testować physical path, endpoint i events bez reinstall-all.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Testować physical path, endpoint i events bez reinstall-all.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Rollback/update właściwego OEM audio stack. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Playback/recording i sleep/wake działają. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
przegrzewający się port/kabel, uszkodzenie mechaniczne, managed print policy, kamera/mikrofon z policy privacy.

## windows-peripherals-repair-pb-03: USB/Bluetooth rozłącza

**Objaw i zakres:** Urządzenie znika okresowo.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
przegrzewający się port/kabel, uszkodzenie mechaniczne, managed print policy, kamera/mikrofon z policy privacy. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- problem device IDs.
- port/cable/dock path.
- driver and firmware.
- service/event logs.
- privacy policy.
- known-good peripheral.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Power management, kabel, hub, RF, driver lub hardware.**, wykonaj tylko test: Korelować PnP events i topologię; test znanego kabla/portu.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Korelować PnP events i topologię; test znanego kabla/portu.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Zmieniać jeden element; ustawienia zasilania jako R1 z rollback. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Brak disconnect w powtarzalnym teście oraz po resume. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
przegrzewający się port/kabel, uszkodzenie mechaniczne, managed print policy, kamera/mikrofon z policy privacy.
