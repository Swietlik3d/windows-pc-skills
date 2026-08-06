# Playbooki: Sterowniki i urządzenia

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-drivers-devices-pb-01: Unknown device Code 28

**Objaw i zakres:** Brak sterownika.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage/network driver needed for recovery, managed OEM policy, unsigned driver, BitLocker/boot-critical driver, unknown hardware ID. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- hardware IDs.
- problem code.
- driver provider/version/date.
- SetupAPI excerpt.
- OEM model.
- recent changes.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Hardware ID wskazuje vendor/device.**, wykonaj tylko test: Zebrać IDs i dokładny model; szukać OEM/Windows Update Catalog.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać IDs i dokładny model; szukać OEM/Windows Update Catalog.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Zainstalować podpisany driver właściwy dla arch/build. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Problem code 0 i funkcja urządzenia działa po reboot. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage/network driver needed for recovery, managed OEM policy, unsigned driver, BitLocker/boot-critical driver, unknown hardware ID.

## windows-drivers-devices-pb-02: GPU Code 43

**Objaw i zakres:** Adapter zatrzymany.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage/network driver needed for recovery, managed OEM policy, unsigned driver, BitLocker/boot-critical driver, unknown hardware ID. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- hardware IDs.
- problem code.
- driver provider/version/date.
- SetupAPI excerpt.
- OEM model.
- recent changes.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Driver, firmware, hardware lub passthrough.**, wykonaj tylko test: Sprawdzić pre-OS obraz, WHEA, driver history i clean profile.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Sprawdzić pre-OS obraz, WHEA, driver history i clean profile.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Rollback/OEM clean install; DDU dopiero kontrolowanie. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Brak Code 43 i test GPU bez artefaktów. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage/network driver needed for recovery, managed OEM policy, unsigned driver, BitLocker/boot-critical driver, unknown hardware ID.

## windows-drivers-devices-pb-03: Driver powoduje boot loop

**Objaw i zakres:** Po aktualizacji system nie startuje.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage/network driver needed for recovery, managed OEM policy, unsigned driver, BitLocker/boot-critical driver, unknown hardware ID. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- hardware IDs.
- problem code.
- driver provider/version/date.
- SetupAPI excerpt.
- OEM model.
- recent changes.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Ostatni OEM INF jest niekompatybilny.**, wykonaj tylko test: WinRE/offline SetupAPI i driver store inventory.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** WinRE/offline SetupAPI i driver store inventory.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Usunąć tylko wskazany published name przez wrapper R3. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Boot, device function i no new errors. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage/network driver needed for recovery, managed OEM policy, unsigned driver, BitLocker/boot-critical driver, unknown hardware ID.
