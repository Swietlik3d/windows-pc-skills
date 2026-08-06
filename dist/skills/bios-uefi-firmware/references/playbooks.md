# Playbooki: BIOS, UEFI i firmware

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## bios-uefi-firmware-pb-01: Zmiana Secure Boot po aktualizacji

**Objaw i zakres:** Secure Boot jest wyłączony lub status nieznany.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
niepewny model/rewizja, niestabilne zasilanie, brak BitLocker key readiness, przerwany poprzedni flash. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- manufacturer/model/board revision.
- wersja BIOS i EC.
- tryb UEFI/Legacy.
- Secure Boot/TPM.
- BitLocker protectors bez kluczy.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **CSM, klucze firmware albo polityka OEM.**, wykonaj tylko test: Zebrać msinfo32/Confirm-SecureBootUEFI i stan BitLocker.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać msinfo32/Confirm-SecureBootUEFI i stan BitLocker.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Najpierw firmware OEM; zmianę kluczy wykonać dopiero po planie recovery. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Secure Boot i boot działają, BitLocker nie żąda niespodziewanie recovery. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
niepewny model/rewizja, niestabilne zasilanie, brak BitLocker key readiness, przerwany poprzedni flash.

## bios-uefi-firmware-pb-02: Plan aktualizacji BIOS

**Objaw i zakres:** OEM zaleca poprawkę stabilności.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
niepewny model/rewizja, niestabilne zasilanie, brak BitLocker key readiness, przerwany poprzedni flash. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- manufacturer/model/board revision.
- wersja BIOS i EC.
- tryb UEFI/Legacy.
- Secure Boot/TPM.
- BitLocker protectors bez kluczy.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Właściwy obraz zależy od dokładnej rewizji.**, wykonaj tylko test: Zweryfikować Service Tag/model/board, release notes i podpis.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zweryfikować Service Tag/model/board, release notes i podpis.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Flash pozostawić ręcznej, jawnie potwierdzonej procedurze R4. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Po flashu sprawdzić wersję, ustawienia, TPM, boot i temperatury. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
niepewny model/rewizja, niestabilne zasilanie, brak BitLocker key readiness, przerwany poprzedni flash.

## bios-uefi-firmware-pb-03: Boot order po wymianie dysku

**Objaw i zakres:** UEFI nie pokazuje Windows Boot Manager.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
niepewny model/rewizja, niestabilne zasilanie, brak BitLocker key readiness, przerwany poprzedni flash. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- manufacturer/model/board revision.
- wersja BIOS i EC.
- tryb UEFI/Legacy.
- Secure Boot/TPM.
- BitLocker protectors bez kluczy.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Brak wpisu NVRAM, niewłaściwy tryb lub ESP.**, wykonaj tylko test: Najpierw udokumentować layout i firmware mode.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Najpierw udokumentować layout i firmware mode.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Naprawę BCD przekazać do dedykowanego skilla; nie przełączać CSM w ciemno. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Windows Boot Manager wskazuje właściwy ESP i startuje trzy razy. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
niepewny model/rewizja, niestabilne zasilanie, brak BitLocker key readiness, przerwany poprzedni flash.
