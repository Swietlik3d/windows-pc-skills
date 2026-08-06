# Playbooki: Setup, upgrade i rollback

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-setup-upgrade-rollback-pb-01: Feature update rollback

**Objaw i zakres:** Setup wraca do poprzedniego builda.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak backupu, storage/RAM instability, BitLocker not ready, unsupported hardware bypass, managed safeguard hold. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- SetupDiag result.
- Panther/Rollback logs.
- compat scan.
- build/edition/language.
- drivers/apps.
- free space.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Rule match wskazuje driver/app/partition.**, wykonaj tylko test: Uruchomić parser na kopii logów i potwierdzić fazę.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Uruchomić parser na kopii logów i potwierdzić fazę.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Usunąć tylko potwierdzony blocker lub zaktualizować OEM driver. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Upgrade kończy OOBE/login i zachowuje dane/aplikacje. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak backupu, storage/RAM instability, BitLocker not ready, unsupported hardware bypass, managed safeguard hold.

## windows-setup-upgrade-rollback-pb-02: In-place repair install

**Objaw i zakres:** System działa, component repair nie wystarcza.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak backupu, storage/RAM instability, BitLocker not ready, unsupported hardware bypass, managed safeguard hold. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- SetupDiag result.
- Panther/Rollback logs.
- compat scan.
- build/edition/language.
- drivers/apps.
- free space.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Repair install może zachować apps/data, ale wymaga zgodnego media.**, wykonaj tylko test: Sprawdzić edition/language/build, backup i BitLocker.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Sprawdzić edition/language/build, backup i BitLocker.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Uruchomienie pozostawić jawnej interakcji z Setup; nie automatyzować wyborów. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Build, activation, apps, profile i update działają. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak backupu, storage/RAM instability, BitLocker not ready, unsupported hardware bypass, managed safeguard hold.

## windows-setup-upgrade-rollback-pb-03: Compatibility hold

**Objaw i zakres:** Windows Update nie oferuje wersji.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak backupu, storage/RAM instability, BitLocker not ready, unsupported hardware bypass, managed safeguard hold. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- SetupDiag result.
- Panther/Rollback logs.
- compat scan.
- build/edition/language.
- drivers/apps.
- free space.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Microsoft/OEM safeguard może być zamierzony.**, wykonaj tylko test: Sprawdzić release health i SetupCompat logs.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Sprawdzić release health i SetupCompat logs.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nie wymuszać bypass; poczekać lub zastosować oficjalną poprawkę. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Hold znika oficjalnie albo decyzja o pozostaniu jest udokumentowana. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak backupu, storage/RAM instability, BitLocker not ready, unsupported hardware bypass, managed safeguard hold.
