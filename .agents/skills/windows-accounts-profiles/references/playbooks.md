# Playbooki: Konta, logowanie i profile

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-accounts-profiles-pb-01: Temporary profile

**Objaw i zakres:** Windows loguje do profilu tymczasowego.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak autoryzacji właściciela, EFS, Entra/MDM, brak kopii profilu, podejrzenie account compromise. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- account type/source.
- profile SID/path/state.
- User Profile Service events.
- EFS awareness.
- MSA/Entra recovery channel.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **ProfileList state/path, disk/ACL lub hive corruption.**, wykonaj tylko test: Zebrać events i profile mapping, sprawdzić storage.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać events i profile mapping, sprawdzić storage.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Najpierw odwracalna korekta pojedynczego mappingu; migracja do nowego profilu jeśli hive uszkodzony. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Dwa logowania do właściwego profilu i aplikacje/dane dostępne. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak autoryzacji właściciela, EFS, Entra/MDM, brak kopii profilu, podejrzenie account compromise.

## windows-accounts-profiles-pb-02: Hello PIN unavailable

**Objaw i zakres:** PIN nie działa po TPM/firmware change.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak autoryzacji właściciela, EFS, Entra/MDM, brak kopii profilu, podejrzenie account compromise. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- account type/source.
- profile SID/path/state.
- User Profile Service events.
- EFS awareness.
- MSA/Entra recovery channel.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Hello container, TPM attestation lub policy.**, wykonaj tylko test: Potwierdzić password/official recovery i stan TPM/Entra.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Potwierdzić password/official recovery i stan TPM/Entra.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Użyć oficjalnego „I forgot my PIN”; nie usuwać NGC w ciemno. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

PIN re-enrolled, password fallback i access policies działają. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak autoryzacji właściciela, EFS, Entra/MDM, brak kopii profilu, podejrzenie account compromise.

## windows-accounts-profiles-pb-03: Migracja uszkodzonego profilu

**Objaw i zakres:** Explorer/apps padają tylko dla jednego usera.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak autoryzacji właściciela, EFS, Entra/MDM, brak kopii profilu, podejrzenie account compromise. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- account type/source.
- profile SID/path/state.
- User Profile Service events.
- EFS awareness.
- MSA/Entra recovery channel.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **User hive/profile corruption.**, wykonaj tylko test: Porównać nowy test profile i zinwentaryzować EFS/OneDrive.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Porównać nowy test profile i zinwentaryzować EFS/OneDrive.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Migrować dane, nie cały AppData/registry; zachować ACL. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Nowy profil działa, dane otwierają się, sync i backup zweryfikowane. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak autoryzacji właściciela, EFS, Entra/MDM, brak kopii profilu, podejrzenie account compromise.
