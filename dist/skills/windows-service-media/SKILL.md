---
name: windows-service-media
description: "Prowadzi bezpieczną diagnostykę i kontrolowane działania dla: projekt oficjalnego WinPE lub multiboot USB z manifestem, licencjami, SHA-256/signature i rozdzieleniem x64/ARM64. Aktywuj przy zgłoszeniach: zrób pendrive serwisowy; WinPE toolkit; service USB; herstel-USB maken. Use for Windows service diagnostics in this domain; do not use outside this scope. Zawsze zaczynaj od ochrony danych i dowodów."
metadata:
  swietlik.orchestrator.schema: "1"
  swietlik.orchestrator.pack: "windows-pc-skills"
  swietlik.orchestrator.recommended-agent: "expert_worker"
  swietlik.orchestrator.minimum-agent: "expert_worker"
  swietlik.orchestrator.reasoning: "high"
  swietlik.orchestrator.verbosity: "medium"
  swietlik.orchestrator.delegation: "preferred"
  swietlik.orchestrator.review: "required"
  swietlik.orchestrator.parallel: "forbidden"
  swietlik.orchestrator.risk: "high"
---

# Bezpieczny nośnik serwisowy

## Cel i granice odpowiedzialności

Prowadź projekt oficjalnego WinPE lub multiboot USB z manifestem, licencjami, SHA-256/signature i rozdzieleniem x64/ARM64. Rozdzielaj fakty, hipotezy, testy i wyniki. Nie wykonuj zmian bez
autoryzacji odpowiedniej do R0–R4. Nie pobierać ISO/binariów ani nie zapisywać USB bez jawnego polecenia i potwierdzenia celu.

## Kiedy aktywować i kiedy nie aktywować

Aktywuj dla fraz: `zrób pendrive serwisowy`, `WinPE toolkit`, `service USB`, `herstel-USB maken`. Nie aktywuj dla
problemów, których główna przyczyna należy do powiązanego skilla; router wybiera dokładnie jeden
skill główny. Użytkowanie jawne `$$windows-service-media` ma pierwszeństwo, ale nie znosi bramek bezpieczeństwa.

## Dane wejściowe i minimalne pytania bezpieczeństwa

Najpierw ustal: czy system startuje; czy istnieje zweryfikowany backup; czy dane są cenniejsze niż
urządzenie; czy BitLocker/Device Encryption jest włączony; czy urządzenie jest domain/Entra/MDM;
jakie były ostatnie zmiany; jaki dokładnie objaw i czas reprodukcji. Nie pytaj o recovery key,
hasło, token ani pełny product key. Dla tej domeny zbierz:

- target unique ID/capacity.
- media manifest.
- official URLs.
- license/redistribution.
- checksums/signatures.
- UEFI/BIOS/arch.

## Szybki triage i czerwone flagi

- **STOP:** nieustalony target USB.
- **STOP:** brak backupu nośnika.
- **STOP:** narzędzie redistribution forbidden.
- **STOP:** niezweryfikowany checksum.
- **STOP:** Secure Boot incompatibility.

Jeżeli wystąpi flaga, zatrzymaj testy, zabezpiecz dowody i przejdź do eskalacji. Nie interpretuj
braku telemetrii jako potwierdzenia zdrowia.

## Zgodność

Obsługuj Windows XP SP3–11, ale przed komendą sprawdź build, edition, x86/x64/ARM64, język,
online/Safe Mode/WinRE/WinPE/offline oraz BIOS/MBR albo UEFI/GPT. Najpierw otwórz
[references/compatibility.md](references/compatibility.md), gdy środowisko jest legacy, offline,
ARM64, w trybie S, N, LTSC/LTSB lub zarządzane. W WinRE nigdy nie zakładaj `C:`.

## Drzewo objaw → dowód → hipoteza → test

1. **Objaw:** ADK i add-on mogą być zainstalowane. → **hipoteza:** Wersja ADK musi pasować scenariuszowi i mieć poprawki. → **test:** Wykryć lokalnie ADK bez instalacji/pobierania. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.
2. **Objaw:** Technik chce kilka legalnych obrazów. → **hipoteza:** Secure Boot/licencje/integralność różnią się per asset. → **test:** Zweryfikować każde źródło, hash i redistribution. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.
3. **Objaw:** Narzędzia mogły się zestarzeć. → **hipoteza:** Stale/EOL tool może być ryzykiem. → **test:** Porównać katalog z official release pages i diff do review. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.

Pełne rozgałęzienia znajdują się w [references/playbooks.md](references/playbooks.md). Otwórz tylko
playbook pasujący do objawu; nie ładuj wszystkich referencji.

## Najpierw diagnostyka read-only

1. Zamroź zakres i zapisz baseline/timeline.
2. Zbierz minimalny zestaw R0 bez czyszczenia logów.
3. Oceń storage, RAM, zasilanie i termikę, jeżeli mogą fałszować diagnozę.
4. Zrankuj maksymalnie trzy hipotezy i zapisz dowód za/przeciw.
5. Zmień jedną istotną zmienną dopiero po mierzalnym teście.

## Drabina napraw

1. **R0:** obserwacja, eksport, reprodukcja, porównanie.
2. **R1:** odwracalna zmiana użytkownika z zapisanym stanem before.
3. **R2:** kontrolowana zmiana systemowa; backup, `-WhatIf`/`Scan`, `-Apply`, rollback.
4. **R3:** naprawa wysokiego ryzyka; jawne potwierdzenie celu, BitLocker readiness i kopia.
5. **R4:** destrukcja/firmware; nigdy automatycznie, tylko dokładny cel i wpisane potwierdzenie.

Nie przeskakuj szczebla bez dowodu, że niższy nie może spełnić kryterium sukcesu.

## Karty poleceń

- `Plan media` — Repo — PowerShell 5.1+, R0; szczegóły w [references/command-cards.md](references/command-cards.md#plan-media).
- `Integrity` — Repo — PowerShell 5.1+, R0; szczegóły w [references/command-cards.md](references/command-cards.md#integrity).
- `Verified download plan` — Repo — PowerShell 5.1+, R0; szczegóły w [references/command-cards.md](references/command-cards.md#verified-download-plan).

Każdy blok podaj z kontekstem wykonania. Używaj placeholderów `<TARGET>`, `<OS_VOLUME>` i
`<OUTPUT>`; przed R2+ pokaż rozwinięte wartości do potwierdzenia.

## Dlaczego to może pójść źle

Pomylenie środowiska, celu, architektury, edycji lub źródła może zmienić niewłaściwy system.
Brak backupu może zamienić naprawę w utratę danych. Restart lub intensywny test może pogorszyć
awarię sprzętową. Narzędzie community może wykonywać więcej zmian niż deklaruje. Z tego powodu
wykonuj preflight, zapisuj dokładny command/tool version i przerywaj przy odchyleniu.

## Backup i rollback przed zmianą

Zapisz konfigurację before, hash artefaktu, log, dokładny cel, przewidywany skutek i komendę
rollback. Nie nazywaj punktu przywracania jedynym backupem. Dla danych użyj niezależnej kopii;
dla BCD/ACL/registry/driver exportuj dokładny obiekt. Jeżeli rollback nie jest możliwy, podnieś
klasę ryzyka i poproś o jawne potwierdzenie.

## Oczekiwany wynik i interpretacja

Każdy etap ma zwrócić: `observed`, `not-observed`, `inconclusive` albo `blocked`. Brak błędu nie
oznacza naprawy; porównaj z baseline. Jeżeli wynik nie pasuje do hipotezy, nie powtarzaj zmiany —
cofnij ją i przelicz ranking.

## Walidacja i regresja

Powtórz test przyczyny, test dokładnego objawu oraz test regresji dla boot/restart, sleep/wake,
sieci, zabezpieczeń, backupu i dotkniętych peryferiów. Zapisz liczbę prób i czas. Użyj
[`windows-post-repair-validation`](../windows-post-repair-validation/SKILL.md) przed statusem
`fixed`.

## Przerwanie i eskalacja

Przerwij przy czerwonej fladze, utracie łączności z celem, rosnących błędach, niezgodnym output,
braku autoryzacji albo niedostępnym rollbacku. Eskaluj hardware component-level do elektronika,
odzysk krytycznych danych do laboratorium, urządzenia firmowe do administratora, a incydent do
IR/forensics. Nie improwizuj obejść ochrony.

## Logi i artefakty

Zachowaj: intake/authorization, timeline UTC, baseline, polecenia i wersje narzędzi, output
stdout/stderr, relevant event/log extracts, hashes, before/after, wynik rollback testu i ryzyko
resztkowe. Anonimizuj domyślnie. Nie zapisuj haseł, cookies, tokens, recovery keys ani pełnych
kluczy produktu.

## Powiązane skille

- [`windows-tool-research`](../windows-tool-research/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`windows-deployment-imaging`](../windows-deployment-imaging/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`bios-uefi-firmware`](../bios-uefi-firmware/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`windows-automation-powershell`](../windows-automation-powershell/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.

## Źródła

- `ms-adk` — [Download and install Windows ADK](https://learn.microsoft.com/en-us/windows-hardware/get-started/adk-install) (zweryfikowano 2026-08-06).
- `ms-winpe` — [Windows PE overview](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/winpe-intro) (zweryfikowano 2026-08-06).
- `rufus` — [Rufus](https://github.com/pbatard/rufus) (zweryfikowano 2026-08-06).
- `ventoy` — [Ventoy download](https://www.ventoy.net/en/download.html) (zweryfikowano 2026-08-06).

Szczegóły i claim scope: [references/sources.md](references/sources.md). Informacje zależne od
wersji ponownie zweryfikuj, jeżeli snapshot ma ponad 90 dni.

## Antywzorce

- Nie uruchamiaj „one-click repair”, debloat ani kilku skanerów równocześnie.
- Nie używaj `Win32_Product`, `Invoke-Expression`, pipe-to-shell ani przypadkowego driver pack.
- Nie czyść logów i nie resetuj całej konfiguracji przed zebraniem dowodów.
- Nie wyłączaj trwale Defendera, Firewall, Update, UAC, SmartScreen, Secure Boot ani HVCI.
- Nie przedstawiaj community workaround jako wspieranej naprawy bez drugiego źródła/lab.

## Format odpowiedzi

Odpowiedz kolejno: `Najpierw zabezpiecz`, `Co obecnie wiemy`, `Najbardziej prawdopodobne
przyczyny`, `Krok diagnostyczny`, `Oczekiwany wynik`, `Naprawa`, `Rollback`, `Sprawdzenie`,
`Pozostałe ryzyko`. Prowadź jedną fazę na raz i podawaj poziom pewności.
