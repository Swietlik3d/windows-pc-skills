# Playbooki: RAM, CPU, GPU i termika

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## memory-cpu-gpu-thermal-pb-01: Losowe restarty pod obciążeniem

**Objaw i zakres:** PC resetuje się bez BSOD.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
jakikolwiek błąd RAM, temperatura szybko rośnie do limitu, zapach/wyciek chłodziwa, niestabilne OC przy danych krytycznych. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- WHEA timeline.
- temperatury i clocks.
- ustawienia stock/XMP.
- moduły i sloty.
- sterownik GPU.
- zasilanie.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **PSU, termika, RAM lub zabezpieczenie VRM.**, wykonaj tylko test: Zebrać WHEA/Kernel-Power i temperatury, testować jeden podsystem.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zebrać WHEA/Kernel-Power i temperatury, testować jeden podsystem.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Wrócić do stock; wymienić znaną dobrą część przed zmianami systemu. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Brak restartu w powtarzalnym obciążeniu i zimnym starcie. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
jakikolwiek błąd RAM, temperatura szybko rośnie do limitu, zapach/wyciek chłodziwa, niestabilne OC przy danych krytycznych.

## memory-cpu-gpu-thermal-pb-02: Błędy MemTest

**Objaw i zakres:** Co najmniej jeden błąd pamięci.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
jakikolwiek błąd RAM, temperatura szybko rośnie do limitu, zapach/wyciek chłodziwa, niestabilne OC przy danych krytycznych. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- WHEA timeline.
- temperatury i clocks.
- ustawienia stock/XMP.
- moduły i sloty.
- sterownik GPU.
- zasilanie.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Moduł, slot, IMC lub niestabilny profil.**, wykonaj tylko test: Zatrzymać diagnozę software i powtórzyć na stock po jednym module.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zatrzymać diagnozę software i powtórzyć na stock po jednym module.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Wymienić wadliwy element lub obniżyć do wspieranej konfiguracji. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Wiele pełnych przejść bez błędów oraz test systemowy. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
jakikolwiek błąd RAM, temperatura szybko rośnie do limitu, zapach/wyciek chłodziwa, niestabilne OC przy danych krytycznych.

## memory-cpu-gpu-thermal-pb-03: Artefakty GPU

**Objaw i zakres:** Kolorowe bloki w BIOS i Windows.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
jakikolwiek błąd RAM, temperatura szybko rośnie do limitu, zapach/wyciek chłodziwa, niestabilne OC przy danych krytycznych. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- WHEA timeline.
- temperatury i clocks.
- ustawienia stock/XMP.
- moduły i sloty.
- sterownik GPU.
- zasilanie.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **GPU/VRAM/hardware bardziej prawdopodobny niż sterownik.**, wykonaj tylko test: Porównać obraz przed ładowaniem OS i na innym kablu/monitorze.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Porównać obraz przed ładowaniem OS i na innym kablu/monitorze.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Jeśli tylko Windows — clean driver path; jeśli pre-OS — wymiana/eskalacja. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Brak artefaktów w pre-OS i kontrolowanym teście GPU. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
jakikolwiek błąd RAM, temperatura szybko rośnie do limitu, zapach/wyciek chłodziwa, niestabilne OC przy danych krytycznych.
