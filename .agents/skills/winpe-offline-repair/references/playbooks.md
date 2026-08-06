# Playbooki: WinRE, WinPE i naprawa offline

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## winpe-offline-repair-pb-01: Ustalenie litery offline OS

**Objaw i zakres:** WinRE pokazuje wiele NTFS.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
nieustalone źródło/cel, BitLocker locked, storage risk, hive już załadowany, źródło DISM nie pasuje. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- disk/volume unique IDs.
- OS directory.
- BCD device.
- BitLocker lock state.
- build/language/index.
- wolne miejsce.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Litery zostały przypisane dynamicznie.**, wykonaj tylko test: Listować woluminy i potwierdzić Windows dir, SOFTWARE hive i BCD.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Listować woluminy i potwierdzić Windows dir, SOFTWARE hive i BCD.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Zapisać mapę do sprawy; nie używać domyślnego C:. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Trzy niezależne sygnały wskazują ten sam OS volume. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
nieustalone źródło/cel, BitLocker locked, storage risk, hive już załadowany, źródło DISM nie pasuje.

## winpe-offline-repair-pb-02: Eksport logów offline

**Objaw i zakres:** Windows nie startuje, potrzebne CBS/Panther.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
nieustalone źródło/cel, BitLocker locked, storage risk, hive już załadowany, źródło DISM nie pasuje. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- disk/volume unique IDs.
- OS directory.
- BCD device.
- BitLocker lock state.
- build/language/index.
- wolne miejsce.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Logi mogą wskazać przyczynę bez zmiany systemu.**, wykonaj tylko test: Skopiować wybrane pliki z zachowaniem czasów i hashy.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Skopiować wybrane pliki z zachowaniem czasów i hashy.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Pracować na kopii, zanonimizować raport. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Manifest zawiera źródło, rozmiar i SHA-256. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
nieustalone źródło/cel, BitLocker locked, storage risk, hive już załadowany, źródło DISM nie pasuje.

## winpe-offline-repair-pb-03: Offline component repair

**Objaw i zakres:** CBS wskazuje corruption, storage/RAM stabilne.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
nieustalone źródło/cel, BitLocker locked, storage risk, hive już załadowany, źródło DISM nie pasuje. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- disk/volume unique IDs.
- OS directory.
- BCD device.
- BitLocker lock state.
- build/language/index.
- wolne miejsce.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Źródło musi pasować build/edition/language.**, wykonaj tylko test: Najpierw DISM Check/Scan na wskazanym image i zweryfikować source index.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Najpierw DISM Check/Scan na wskazanym image i zweryfikować source index.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Apply dopiero R2 po snapshot/backup i planie rollback. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

DISM/SFC exit, logs i ponowny boot są zweryfikowane. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
nieustalone źródło/cel, BitLocker locked, storage risk, hive już załadowany, źródło DISM nie pasuje.
