# Playbooki: Identyfikacja Windows

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-os-identification-pb-01: System online

**Objaw i zakres:** Windows działa, wersja nieznana.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
wyniki z różnych instalacji/offline volume, WinRE z nieustaloną literą, build poza matrycą, tryb S lub organizacyjne policy. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- ProductName/EditionID.
- CurrentBuild/UBR.
- architecture.
- locale.
- FirmwareType.
- partition style.
- WinRE status.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Nazwa marketingowa może nie odpowiadać buildowi.**, wykonaj tylko test: Zebrać rejestr, systeminfo i architekturę; porównać z release matrix.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać rejestr, systeminfo i architekturę; porównać z release matrix.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nie zakładać support na podstawie samego ProductName. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Raport zawiera edition, build.UBR, kanał i datę weryfikacji. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
wyniki z różnych instalacji/offline volume, WinRE z nieustaloną literą, build poza matrycą, tryb S lub organizacyjne policy.

## windows-os-identification-pb-02: System offline w WinRE

**Objaw i zakres:** Litery dysków są inne.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
wyniki z różnych instalacji/offline volume, WinRE z nieustaloną literą, build poza matrycą, tryb S lub organizacyjne policy. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- ProductName/EditionID.
- CurrentBuild/UBR.
- architecture.
- locale.
- FirmwareType.
- partition style.
- WinRE status.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **C: może być WinRE, nie Windows.**, wykonaj tylko test: Przeszukać woluminy read-only po Windows/System32/config/SOFTWARE.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Przeszukać woluminy read-only po Windows/System32/config/SOFTWARE.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Załadować hive pod unikalną nazwą tylko do odczytu i zawsze odmontować. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Wskazany OS_VOLUME ma zgodny BCD, Windows dir i build. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
wyniki z różnych instalacji/offline volume, WinRE z nieustaloną literą, build poza matrycą, tryb S lub organizacyjne policy.

## windows-os-identification-pb-03: ARM64/S mode/N edition

**Objaw i zakres:** Aplikacja lub sterownik nie działa.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
wyniki z różnych instalacji/offline volume, WinRE z nieustaloną literą, build poza matrycą, tryb S lub organizacyjne policy. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- ProductName/EditionID.
- CurrentBuild/UBR.
- architecture.
- locale.
- FirmwareType.
- partition style.
- WinRE status.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Ograniczenie może wynikać z architektury albo edycji.**, wykonaj tylko test: Ustalić native arch, emulation i capability edition.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Ustalić native arch, emulation i capability edition.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Dobrać tylko kompatybilne narzędzia; nie obchodzić S mode. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Rekomendacja ma jawny wpis kompatybilności. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
wyniki z różnych instalacji/offline volume, WinRE z nieustaloną literą, build poza matrycą, tryb S lub organizacyjne policy.
