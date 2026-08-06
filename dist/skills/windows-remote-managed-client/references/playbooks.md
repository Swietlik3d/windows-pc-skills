# Playbooki: Klient zdalny, domenowy, Entra i MDM

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-remote-managed-client-pb-01: Quick Assist session

**Objaw i zakres:** Użytkownik prosi o widoczną pomoc.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak świadomej zgody na sesję, Defender for Endpoint/LAPS/MDM, certificate/private key, conditional access, organizational data. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- join state.
- MDM enrollment.
- gpresult.
- cert store metadata bez private keys.
- VPN/mapped drive.
- session consent.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Sesja musi być świadoma i odwracalna.**, wykonaj tylko test: Potwierdzić zakres, recording/data access i zakończenie.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Potwierdzić zakres, recording/data access i zakończenie.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nie instalować trwałego agenta; każdą zmianę zapisać. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Użytkownik widzi zakończenie, session closed, actions reported. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak świadomej zgody na sesję, Defender for Endpoint/LAPS/MDM, certificate/private key, conditional access, organizational data.

## windows-remote-managed-client-pb-02: GPO nie stosuje się

**Objaw i zakres:** Firmowa konfiguracja brakująca.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak świadomej zgody na sesję, Defender for Endpoint/LAPS/MDM, certificate/private key, conditional access, organizational data. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- join state.
- MDM enrollment.
- gpresult.
- cert store metadata bez private keys.
- VPN/mapped drive.
- session consent.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Connectivity, time, trust, scope lub client extension.**, wykonaj tylko test: gpresult/events/domain connectivity bez gpupdate force loops.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** gpresult/events/domain connectivity bez gpupdate force loops.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Eskalować z dowodami do admina; nie edytować local policy przeciw GPO. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

RSoP wskazuje oczekiwaną policy lub znany owner blocker. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak świadomej zgody na sesję, Defender for Endpoint/LAPS/MDM, certificate/private key, conditional access, organizational data.

## windows-remote-managed-client-pb-03: Entra/MDM compliance

**Objaw i zakres:** Device noncompliant.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak świadomej zgody na sesję, Defender for Endpoint/LAPS/MDM, certificate/private key, conditional access, organizational data. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- join state.
- MDM enrollment.
- gpresult.
- cert store metadata bez private keys.
- VPN/mapped drive.
- session consent.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Policy, certificate, TPM, update lub stale enrollment.**, wykonaj tylko test: dsregcmd/status i MDM diagnostics bez tokenów.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** dsregcmd/status i MDM diagnostics bez tokenów.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Nie re-enroll/leave organization bez administratora. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Compliance naprawiona oficjalnym kanałem i access restored. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak świadomej zgody na sesję, Defender for Endpoint/LAPS/MDM, certificate/private key, conditional access, organizational data.
