# Playbooki: Bieżące Windows 11

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-11-support-pb-01: Dobór aktywnej gałęzi

**Objaw i zakres:** PC ma 24H2/25H2/26H1.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
26H1 traktowane jako upgrade dla istniejącego PC, Secure Boot cert not updated, BitLocker key not ready, compatibility hold bypass. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- version/build/edition.
- hardware/arch.
- release health.
- Secure Boot/TPM/VBS.
- Device Encryption.
- driver DCH.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **26H1 jest hardware-optimized i nie jest in-place path dla starszych urządzeń.**, wykonaj tylko test: Query dynamic matrix oraz model/OEM path.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Query dynamic matrix oraz model/OEM path.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nie wymuszać niewłaściwej branch; stosować oferowaną ścieżkę. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Build pozostaje wspierany i miesięczne updates działają. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
26H1 traktowane jako upgrade dla istniejącego PC, Secure Boot cert not updated, BitLocker key not ready, compatibility hold bypass.

## windows-11-support-pb-02: ARM64 compatibility

**Objaw i zakres:** Aplikacja/driver nie instaluje.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
26H1 traktowane jako upgrade dla istniejącego PC, Secure Boot cert not updated, BitLocker key not ready, compatibility hold bypass. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- version/build/edition.
- hardware/arch.
- release health.
- Secure Boot/TPM/VBS.
- Device Encryption.
- driver DCH.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Emulacja apps nie obejmuje każdego kernel drivera.**, wykonaj tylko test: Ustalić native arch pakietu i driver support OEM.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Ustalić native arch pakietu i driver support OEM.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Wybrać ARM64/native albo oficjalnie wspierany emulated app. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Funkcja działa bez unsigned/bypass driver. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
26H1 traktowane jako upgrade dla istniejącego PC, Secure Boot cert not updated, BitLocker key not ready, compatibility hold bypass.

## windows-11-support-pb-03: Device Encryption recovery risk

**Objaw i zakres:** Update firmware/security przed zmianą.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
26H1 traktowane jako upgrade dla istniejącego PC, Secure Boot cert not updated, BitLocker key not ready, compatibility hold bypass. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- version/build/edition.
- hardware/arch.
- release health.
- Secure Boot/TPM/VBS.
- Device Encryption.
- driver DCH.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **TPM/Secure Boot PCR może wywołać BitLocker.**, wykonaj tylko test: Safety status, key readiness i management owner.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Safety status, key readiness i management owner.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Pilot/backup/suspend minimalny tylko z zgodą. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Protection resumed i dwa cold boots bez recovery. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
26H1 traktowane jako upgrade dla istniejącego PC, Secure Boot cert not updated, BitLocker key not ready, compatibility hold bypass.
