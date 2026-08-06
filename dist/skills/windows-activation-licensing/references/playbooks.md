# Playbooki: Aktywacja i licencjonowanie Windows

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-activation-licensing-pb-01: Edition mismatch po reinstalacji

**Objaw i zakres:** Licencja Home, zainstalowano Pro.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
prośba o crack/KMS emulator, pełny product key w logu, urządzenie firmowe z volume activation, niejasny dowód licencji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- edition/channel.
- partial product key only.
- activation status/error.
- OEM marker presence bez klucza.
- MSA link.
- organization scope.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Digital entitlement nie aktywuje innej edycji.**, wykonaj tylko test: Zebrać edition/channel i activation error bez pełnego key.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać edition/channel i activation error bez pełnego key.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Zainstalować właściwą legalną edycję lub kupić upgrade. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

slmgr status licensed i edition zgodna z entitlement. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
prośba o crack/KMS emulator, pełny product key w logu, urządzenie firmowe z volume activation, niejasny dowód licencji.

## windows-activation-licensing-pb-02: Digital license po wymianie płyty

**Objaw i zakres:** Activation lost after hardware change.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
prośba o crack/KMS emulator, pełny product key w logu, urządzenie firmowe z volume activation, niejasny dowód licencji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- edition/channel.
- partial product key only.
- activation status/error.
- OEM marker presence bez klucza.
- MSA link.
- organization scope.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Hardware hash uległ zmianie.**, wykonaj tylko test: Użyć oficjalnego Activation Troubleshooter z właścicielem MSA.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Użyć oficjalnego Activation Troubleshooter z właścicielem MSA.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Jeśli OEM non-transferable — eskalować do Microsoft/OEM. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Activation UI pokazuje legalną aktywację. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
prośba o crack/KMS emulator, pełny product key w logu, urządzenie firmowe z volume activation, niejasny dowód licencji.

## windows-activation-licensing-pb-03: Firmowy KMS/MAK

**Objaw i zakres:** Laptop poza siecią nie aktywuje.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
prośba o crack/KMS emulator, pełny product key w logu, urządzenie firmowe z volume activation, niejasny dowód licencji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- edition/channel.
- partial product key only.
- activation status/error.
- OEM marker presence bez klucza.
- MSA link.
- organization scope.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Brak kontaktu z firmowym KMS/VPN lub exhausted MAK.**, wykonaj tylko test: Zebrać channel i generic error; nie testować publicznych serwerów.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać channel i generic error; nie testować publicznych serwerów.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Eskalować do administratora licencji. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Status licensed w autoryzowanej sieci. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
prośba o crack/KMS emulator, pełny product key w logu, urządzenie firmowe z volume activation, niejasny dowód licencji.
