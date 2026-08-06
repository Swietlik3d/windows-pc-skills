# Playbooki: BCD, ESP i partycje startowe

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-bcd-partition-repair-pb-01: Brak Windows Boot Manager UEFI

**Objaw i zakres:** Firmware widzi dysk, ale nie wpis.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
nieustalony dysk/OS/ESP, BitLocker bez klucza, storage risk, hybrydowy/niestandardowy layout, dual boot bez zgody. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- firmware mode.
- disk IDs.
- GPT/MBR.
- ESP/active partition.
- BCD export.
- OS loader path.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Wpis NVRAM lub pliki ESP są brakujące.**, wykonaj tylko test: Potwierdzić GPT, FAT32 ESP i właściwy Windows volume.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Potwierdzić GPT, FAT32 ESP i właściwy Windows volume.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Wyeksportować BCD; użyć BCDBoot tylko z jawnymi /s i /f UEFI. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

NVRAM/ESP wskazuje właściwy loader, trzy zimne starty. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
nieustalony dysk/OS/ESP, BitLocker bez klucza, storage risk, hybrydowy/niestandardowy layout, dual boot bez zgody.

## windows-bcd-partition-repair-pb-02: Legacy MBR po klonowaniu

**Objaw i zakres:** BIOS mówi no bootable device.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
nieustalony dysk/OS/ESP, BitLocker bez klucza, storage risk, hybrydowy/niestandardowy layout, dual boot bez zgody. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- firmware mode.
- disk IDs.
- GPT/MBR.
- ESP/active partition.
- BCD export.
- OS loader path.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Active flag, MBR boot code lub BCD device mismatch.**, wykonaj tylko test: Potwierdzić BIOS mode, MBR i aktywną system partition.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Potwierdzić BIOS mode, MBR i aktywną system partition.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Naprawiać pojedynczy element; nie konwertować do GPT w tym samym kroku. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Boot działa i layout pozostaje zgodny z backupem. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
nieustalony dysk/OS/ESP, BitLocker bez klucza, storage risk, hybrydowy/niestandardowy layout, dual boot bez zgody.

## windows-bcd-partition-repair-pb-03: BCD wskazuje złą partycję

**Objaw i zakres:** 0xc000000e po zmianie dysku.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
nieustalony dysk/OS/ESP, BitLocker bez klucza, storage risk, hybrydowy/niestandardowy layout, dual boot bez zgody. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- firmware mode.
- disk IDs.
- GPT/MBR.
- ESP/active partition.
- BCD export.
- OS loader path.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Identifikator urządzenia jest nieaktualny.**, wykonaj tylko test: Eksport BCD i porównanie osdevice z ustalonym OS volume.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Eksport BCD i porównanie osdevice z ustalonym OS volume.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Użyć wrappera R3 z target IDs i potwierdzeniem. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

bcdedit enum oraz boot log potwierdzają właściwy wpis. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
nieustalony dysk/OS/ESP, BitLocker bez klucza, storage risk, hybrydowy/niestandardowy layout, dual boot bez zgody.
