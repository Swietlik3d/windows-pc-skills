# Playbooki: SFC, DISM i component store

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-component-repair-pb-01: SFC reports corruption

**Objaw i zakres:** SFC /verifyonly wykrywa naruszenia.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage/RAM instability, source build/language/index mismatch, pending reboot, brak miejsca, offline volume nieustalony. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- DISM health.
- CBS/DISM excerpts.
- build/edition/language.
- source metadata/index.
- pending state.
- free space.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Component store lub pliki chronione są uszkodzone.**, wykonaj tylko test: Najpierw parsować CBS i ScanHealth.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Najpierw parsować CBS i ScanHealth.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Naprawić store właściwym źródłem, potem pojedynczy SFC. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

ScanHealth clean, SFC clean i test objawu. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage/RAM instability, source build/language/index mismatch, pending reboot, brak miejsca, offline volume nieustalony.

## windows-component-repair-pb-02: DISM 0x800f081f

**Objaw i zakres:** Source files could not be found.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage/RAM instability, source build/language/index mismatch, pending reboot, brak miejsca, offline volume nieustalony. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- DISM health.
- CBS/DISM excerpts.
- build/edition/language.
- source metadata/index.
- pending state.
- free space.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Źródło nie pasuje lub policy blokuje repair content.**, wykonaj tylko test: Porównać build, edition, language i WIM index.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Porównać build, edition, language i WIM index.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Wskazać jawne /Source:wim:<path>:<index> /LimitAccess po walidacji. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

DISM kończy 0, źródło i hash są zapisane. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage/RAM instability, source build/language/index mismatch, pending reboot, brak miejsca, offline volume nieustalony.

## windows-component-repair-pb-03: Offline corruption

**Objaw i zakres:** System nie bootuje, CBS wskazuje servicing.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
storage/RAM instability, source build/language/index mismatch, pending reboot, brak miejsca, offline volume nieustalony. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- DISM health.
- CBS/DISM excerpts.
- build/edition/language.
- source metadata/index.
- pending state.
- free space.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Pending actions lub mismatch source.**, wykonaj tylko test: Zebrać offline identity i logi przed zmianą.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać offline identity i logi przed zmianą.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Repair wrapper z właściwym ImagePath i source; nie revert pending bez wyjątkowego gate. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Boot, DISM/SFC i update scan przechodzą. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
storage/RAM instability, source build/language/index mismatch, pending reboot, brak miejsca, offline volume nieustalony.
