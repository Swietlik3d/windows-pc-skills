# Playbooki: Sieć Windows

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

## windows-network-repair-pb-01: Link jest, brak internetu

**Objaw i zakres:** Adres jest APIPA lub brak gateway.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
managed VPN/firewall, incydent bezpieczeństwa, brak autoryzacji do capture/Nmap, statyczna konfiguracja bez backupu. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- link/radio.
- IP/gateway/DHCP.
- DNS resolution.
- routes/proxy/VPN.
- firewall profile.
- packet timing.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **DHCP/link VLAN/adapter.**, wykonaj tylko test: Test warstwowy: media, lease, gateway, DNS, HTTPS.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Test warstwowy: media, lease, gateway, DNS, HTTPS.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Naprawić najniższą uszkodzoną warstwę; reset jako późny R2. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Lease poprawny, gateway/DNS/HTTPS działają. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
managed VPN/firewall, incydent bezpieczeństwa, brak autoryzacji do capture/Nmap, statyczna konfiguracja bez backupu.

## windows-network-repair-pb-02: DNS intermittent

**Objaw i zakres:** IP działa, nazwy czasem nie.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
managed VPN/firewall, incydent bezpieczeństwa, brak autoryzacji do capture/Nmap, statyczna konfiguracja bez backupu. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- link/radio.
- IP/gateway/DHCP.
- DNS resolution.
- routes/proxy/VPN.
- firewall profile.
- packet timing.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Resolver, suffix, VPN split DNS lub upstream.**, wykonaj tylko test: Porównać Resolve-DnsName z serwerami i timeline.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Porównać Resolve-DnsName z serwerami i timeline.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Korygować konfigurację tylko po identyfikacji właściciela DNS. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Wielokrotne rozwiązywanie obu stref działa bez leak. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
managed VPN/firewall, incydent bezpieczeństwa, brak autoryzacji do capture/Nmap, statyczna konfiguracja bez backupu.

## windows-network-repair-pb-03: VPN psuje sieć

**Objaw i zakres:** Po rozłączeniu brak dostępu.

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
managed VPN/firewall, incydent bezpieczeństwa, brak autoryzacji do capture/Nmap, statyczna konfiguracja bez backupu. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

- link/radio.
- IP/gateway/DHCP.
- DNS resolution.
- routes/proxy/VPN.
- firewall profile.
- packet timing.
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **Routes, proxy, NRPT lub filter driver pozostał.**, wykonaj tylko test: Snapshot przed/po VPN i diff tras/proxy/adapters.
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** Snapshot przed/po VPN i diff tras/proxy/adapters.
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** Repair klienta VPN/OEM; nie usuwać filtrów w ciemno. Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

Sieć działa przed, w trakcie i po VPN. Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
managed VPN/firewall, incydent bezpieczeństwa, brak autoryzacji do capture/Nmap, statyczna konfiguracja bez backupu.
