# Playbooki: Automatyzacja PowerShell i CMD

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-automation-powershell-pb-01: Nowy collector R0

**Objaw i zakres:** Potrzebny powtarzalny export.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak WhatIf/Apply gate, Invoke-Expression, sekrety w logu, nieustalony target, remoting bez autoryzacji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- PowerShell version.
- OS/arch/elevation.
- target set.
- idempotency state.
- rollback.
- mock coverage.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Deterministyczny output ułatwi diagnozę.**, wykonaj tylko test: Zaprojektować typed parameters, redaction i JSON schema.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Zaprojektować typed parameters, redaction i JSON schema.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Testować tylko fixtures/mocks; live mode pozostawić operatorowi. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Syntax, fixtures, redaction i exit codes przechodzą. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak WhatIf/Apply gate, Invoke-Expression, sekrety w logu, nieustalony target, remoting bez autoryzacji.

## windows-automation-powershell-pb-02: Repair wrapper R2

**Objaw i zakres:** Potrzebna kontrolowana zmiana.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak WhatIf/Apply gate, Invoke-Expression, sekrety w logu, nieustalony target, remoting bez autoryzacji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- PowerShell version.
- OS/arch/elevation.
- target set.
- idempotency state.
- rollback.
- mock coverage.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Błąd targetu może uszkodzić system.**, wykonaj tylko test: Preflight, snapshot, -Mode Scan default, -Apply i ShouldProcess.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Preflight, snapshot, -Mode Scan default, -Apply i ShouldProcess.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Concrete cmdlets w switch, bez eval/string execution. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

WhatIf wykonuje zero mutacji, apply test wyłącznie VM. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak WhatIf/Apply gate, Invoke-Expression, sekrety w logu, nieustalony target, remoting bez autoryzacji.

## windows-automation-powershell-pb-03: Legacy compatibility

**Objaw i zakres:** Skrypt ma działać PS5.1/WinRE.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
brak WhatIf/Apply gate, Invoke-Expression, sekrety w logu, nieustalony target, remoting bez autoryzacji. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- PowerShell version.
- OS/arch/elevation.
- target set.
- idempotency state.
- rollback.
- mock coverage.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Nowsza składnia/API może nie istnieć.**, wykonaj tylko test: Parse pod odpowiednimi language modes i zapewnić minimalny CMD fallback.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Parse pod odpowiednimi language modes i zapewnić minimalny CMD fallback.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Oznaczyć funkcje PS7-only; nie polyfillować niebezpiecznie. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Static parse i VM matrix potwierdzają ścieżki. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
brak WhatIf/Apply gate, Invoke-Expression, sekrety w logu, nieustalony target, remoting bez autoryzacji.
