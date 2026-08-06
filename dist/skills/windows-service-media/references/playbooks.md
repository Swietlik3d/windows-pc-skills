# Playbooki: Bezpieczny nośnik serwisowy

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-service-media-pb-01: Plan oficjalnego WinPE

**Objaw i zakres:** ADK i add-on mogą być zainstalowane.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
nieustalony target USB, brak backupu nośnika, narzędzie redistribution forbidden, niezweryfikowany checksum, Secure Boot incompatibility. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- target unique ID/capacity.
- media manifest.
- official URLs.
- license/redistribution.
- checksums/signatures.
- UEFI/BIOS/arch.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Wersja ADK musi pasować scenariuszowi i mieć poprawki.**, wykonaj tylko test: Wykryć lokalnie ADK bez instalacji/pobierania.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Wykryć lokalnie ADK bez instalacji/pobierania.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Wygenerować plan; build wykonać dopiero jawnie na lab host. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Plan wskazuje ADK version, patch, arch i brak third-party binaries. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
nieustalony target USB, brak backupu nośnika, narzędzie redistribution forbidden, niezweryfikowany checksum, Secure Boot incompatibility.

## windows-service-media-pb-02: Multiboot Ventoy/Rufus

**Objaw i zakres:** Technik chce kilka legalnych obrazów.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
nieustalony target USB, brak backupu nośnika, narzędzie redistribution forbidden, niezweryfikowany checksum, Secure Boot incompatibility. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- target unique ID/capacity.
- media manifest.
- official URLs.
- license/redistribution.
- checksums/signatures.
- UEFI/BIOS/arch.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Secure Boot/licencje/integralność różnią się per asset.**, wykonaj tylko test: Zweryfikować każde źródło, hash i redistribution.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zweryfikować każde źródło, hash i redistribution.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nie pobierać automatycznie restricted assets; zapisy USB jako R4. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Manifest odpowiada plikom i testy UEFI/BIOS w lab przechodzą. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
nieustalony target USB, brak backupu nośnika, narzędzie redistribution forbidden, niezweryfikowany checksum, Secure Boot incompatibility.

## windows-service-media-pb-03: Aktualizacja zestawu

**Objaw i zakres:** Narzędzia mogły się zestarzeć.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
nieustalony target USB, brak backupu nośnika, narzędzie redistribution forbidden, niezweryfikowany checksum, Secure Boot incompatibility. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- target unique ID/capacity.
- media manifest.
- official URLs.
- license/redistribution.
- checksums/signatures.
- UEFI/BIOS/arch.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Stale/EOL tool może być ryzykiem.**, wykonaj tylko test: Porównać katalog z official release pages i diff do review.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Porównać katalog z official release pages i diff do review.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Pobierać dopiero po akceptacji licencji i weryfikacji. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Integrity scan clean, provenance complete, EOL items quarantined. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
nieustalony target USB, brak backupu nośnika, narzędzie redistribution forbidden, niezweryfikowany checksum, Secure Boot incompatibility.
