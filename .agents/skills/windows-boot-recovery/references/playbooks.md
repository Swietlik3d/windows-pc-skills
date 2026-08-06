# Playbooki: Odzyskiwanie startu Windows

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-boot-recovery-pb-01: Automatic Repair loop

**Objaw i zakres:** WinRE uruchamia się przy każdym starcie.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage risk, BitLocker bez key readiness, błędy RAM, nieustalony OS volume, firmware nie widzi dysku. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- etap startu.
- firmware detection.
- boot layout.
- SrtTrail/boot log.
- recent change.
- Safe Mode behavior.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Pending update, driver, component corruption albo storage.**, wykonaj tylko test: Najpierw layout/storage, potem zebrać SrtTrail i pending state.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Najpierw layout/storage, potem zebrać SrtTrail i pending state.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Cofnąć pojedynczą zmianę; BCD tylko przy dowodzie. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Trzy poprawne starty i zachowane logi before/after. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage risk, BitLocker bez key readiness, błędy RAM, nieustalony OS volume, firmware nie widzi dysku.

## windows-boot-recovery-pb-02: Czarny ekran po logowaniu

**Objaw i zakres:** Kursor jest, system odpowiada.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage risk, BitLocker bez key readiness, błędy RAM, nieustalony OS volume, firmware nie widzi dysku. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- etap startu.
- firmware detection.
- boot layout.
- SrtTrail/boot log.
- recent change.
- Safe Mode behavior.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Explorer, display driver, profile lub shell extension.**, wykonaj tylko test: Sprawdzić Ctrl+Shift+Esc, Safe Mode i zdalny event timeline.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Sprawdzić Ctrl+Shift+Esc, Safe Mode i zdalny event timeline.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Przekazać do shell/driver/profile zależnie od dowodu. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Login i Explorer działają na nowym i istniejącym profilu. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage risk, BitLocker bez key readiness, błędy RAM, nieustalony OS volume, firmware nie widzi dysku.

## windows-boot-recovery-pb-03: Restart przed logowaniem

**Objaw i zakres:** Logo pojawia się, potem reset.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage risk, BitLocker bez key readiness, błędy RAM, nieustalony OS volume, firmware nie widzi dysku. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- etap startu.
- firmware detection.
- boot layout.
- SrtTrail/boot log.
- recent change.
- Safe Mode behavior.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Bugcheck ukryty przez auto-restart, driver, RAM/storage.**, wykonaj tylko test: Wyłączyć auto-restart wyłącznie w WinRE menu, zebrać bugcheck/dump.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Wyłączyć auto-restart wyłącznie w WinRE menu, zebrać bugcheck/dump.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Naprawiać potwierdzony komponent, nie maskować restartu. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Start stabilny, dump skonfigurowany, regresja sleep/restart. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage risk, BitLocker bez key readiness, błędy RAM, nieustalony OS volume, firmware nie widzi dysku.
