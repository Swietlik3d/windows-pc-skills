# Playbooki: Windows XP, Vista, 7 i 8.x

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-legacy-xp-vista-7-8-pb-01: NTLDR missing XP

**Objaw i zakres:** BIOS widzi dysk, komunikat przed logo.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
Internet exposure, brak backupu na starym HDD, legacy encryption, brak legalnego media/driver, ancient PSU/battery. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- exact OS/SP/arch.
- BIOS/MBR layout.
- hardware age/health.
- offline malware risk.
- data migration target.
- license/media provenance.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Active partition/boot files/boot.ini lub failing disk.**, wykonaj tylko test: Najpierw health/image, potem layout i read-only boot.ini.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Najpierw health/image, potem layout i read-only boot.ini.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Recovery Console command tylko po backupie i właściwym target. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Boot lub dane migrują; system pozostaje izolowany. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
Internet exposure, brak backupu na starym HDD, legacy encryption, brak legalnego media/driver, ancient PSU/battery.

## windows-legacy-xp-vista-7-8-pb-02: Windows 7 nie bootuje

**Objaw i zakres:** Startup Repair loop.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
Internet exposure, brak backupu na starym HDD, legacy encryption, brak legalnego media/driver, ancient PSU/battery. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- exact OS/SP/arch.
- BIOS/MBR layout.
- hardware age/health.
- offline malware risk.
- data migration target.
- license/media provenance.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **BCD/update/driver/storage.**, wykonaj tylko test: Zebrać logs i health, uwzględnić stare WinRE.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać logs i health, uwzględnić stare WinRE.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Najmniej inwazyjny rollback; plan migracji jako wynik długoterminowy. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Dane skopiowane, system startuje offline lub urządzenie zastąpione. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
Internet exposure, brak backupu na starym HDD, legacy encryption, brak legalnego media/driver, ancient PSU/battery.

## windows-legacy-xp-vista-7-8-pb-03: Migracja z 8.1

**Objaw i zakres:** Aplikacja wymaga starego systemu.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
Internet exposure, brak backupu na starym HDD, legacy encryption, brak legalnego media/driver, ancient PSU/battery. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- exact OS/SP/arch.
- BIOS/MBR layout.
- hardware age/health.
- offline malware risk.
- data migration target.
- license/media provenance.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Hardware/software może nie mieć ścieżki upgrade.**, wykonaj tylko test: Inwentaryzacja danych/licencji/dependencies bez Win32_Product.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Inwentaryzacja danych/licencji/dependencies bez Win32_Product.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Eksport danych i czysta migracja do wspieranego OS/VM izolowanej. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Dane/aplikacja zweryfikowane, legacy host odizolowany. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
Internet exposure, brak backupu na starym HDD, legacy encryption, brak legalnego media/driver, ancient PSU/battery.
