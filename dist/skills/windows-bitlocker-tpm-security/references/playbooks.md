# Playbooki: BitLocker, TPM i zabezpieczenia platformy

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-bitlocker-tpm-security-pb-01: Recovery po firmware change

**Objaw i zakres:** Każdy boot żąda key.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak recovery key readiness, firmware/BCD/partition change, managed policy, podejrzenie kradzieży, EFS/certificate loss. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- protection/lock status bez key.
- protector types bez IDs w raporcie publicznym.
- TPM readiness.
- Secure Boot cert state.
- VBS/HVCI.
- management policy.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **PCR zmienił się albo firmware nie zapisuje ustawień.**, wykonaj tylko test: Nie wpisywać key do logu; zebrać firmware/TPM/events po autoryzowanym unlock.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Nie wpisywać key do logu; zebrać firmware/TPM/events po autoryzowanym unlock.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Naprawić firmware/policy i wykonać oficjalny reseal tylko z adminem. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Dwa cold boots bez recovery i protector active. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak recovery key readiness, firmware/BCD/partition change, managed policy, podejrzenie kradzieży, EFS/certificate loss.

## windows-bitlocker-tpm-security-pb-02: Plan zmiany BIOS/BCD

**Objaw i zakres:** Naprawa R3/R4 może wywołać recovery.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak recovery key readiness, firmware/BCD/partition change, managed policy, podejrzenie kradzieży, EFS/certificate loss. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- protection/lock status bez key.
- protector types bez IDs w raporcie publicznym.
- TPM readiness.
- Secure Boot cert state.
- VBS/HVCI.
- management policy.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **BitLocker będzie chronił zmianę boot chain.**, wykonaj tylko test: Potwierdzić backup, recovery readiness i management owner.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Potwierdzić backup, recovery readiness i management owner.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Suspend na minimalną liczbę rebootów tylko jawnie; resume sprawdzić. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Protection On i test recovery process bez ujawniania key. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak recovery key readiness, firmware/BCD/partition change, managed policy, podejrzenie kradzieży, EFS/certificate loss.

## windows-bitlocker-tpm-security-pb-03: Secure Boot cert 2026

**Objaw i zakres:** Urządzenie może mieć certyfikaty 2011.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak recovery key readiness, firmware/BCD/partition change, managed policy, podejrzenie kradzieży, EFS/certificate loss. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- protection/lock status bez key.
- protector types bez IDs w raporcie publicznym.
- TPM readiness.
- Secure Boot cert state.
- VBS/HVCI.
- management policy.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Brak update 2023 ograniczy przyszłe boot protections.**, wykonaj tylko test: Sprawdzić oficjalne signals/events i firmware compatibility.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Sprawdzić oficjalne signals/events i firmware compatibility.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Pilotować oficjalny update, nie wgrywać losowych kluczy. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Status Updated, boot/BitLocker stabilne po kontrolowanych rebootach. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak recovery key readiness, firmware/BCD/partition change, managed policy, podejrzenie kradzieży, EFS/certificate loss.
