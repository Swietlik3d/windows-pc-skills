---
name: windows-boot-recovery
description: "Prowadzi bezpieczną diagnostykę i kontrolowane działania dla: diagnozę etapów boot, Automatic Repair loop, Safe Mode, czarnego ekranu, restartów i SrtTrail bez ślepej przebudowy BCD. Aktywuj przy zgłoszeniach: Automatic Repair loop; Windows nie startuje; zwart scherm na aanmelden; SrtTrail.txt. Use for Windows service diagnostics in this domain; do not use outside this scope. Zawsze zaczynaj od ochrony danych i dowodów."
---

# Odzyskiwanie startu Windows

## Cel i granice odpowiedzialności

Prowadź diagnozę etapów boot, Automatic Repair loop, Safe Mode, czarnego ekranu, restartów i SrtTrail bez ślepej przebudowy BCD. Rozdzielaj fakty, hipotezy, testy i wyniki. Nie wykonuj zmian bez
autoryzacji odpowiedniej do R0–R4. Nie przebudowywać partycji/BCD; przekazać potwierdzoną awarię boot files do dedykowanego skilla.

## Kiedy aktywować i kiedy nie aktywować

Aktywuj dla fraz: `Automatic Repair loop`, `Windows nie startuje`, `zwart scherm na aanmelden`, `SrtTrail.txt`. Nie aktywuj dla
problemów, których główna przyczyna należy do powiązanego skilla; router wybiera dokładnie jeden
skill główny. Użytkowanie jawne `$$windows-boot-recovery` ma pierwszeństwo, ale nie znosi bramek bezpieczeństwa.

## Dane wejściowe i minimalne pytania bezpieczeństwa

Najpierw ustal: czy system startuje; czy istnieje zweryfikowany backup; czy dane są cenniejsze niż
urządzenie; czy BitLocker/Device Encryption jest włączony; czy urządzenie jest domain/Entra/MDM;
jakie były ostatnie zmiany; jaki dokładnie objaw i czas reprodukcji. Nie pytaj o recovery key,
hasło, token ani pełny product key. Dla tej domeny zbierz:

- etap startu.
- firmware detection.
- boot layout.
- SrtTrail/boot log.
- recent change.
- Safe Mode behavior.

## Szybki triage i czerwone flagi

- **STOP:** storage risk.
- **STOP:** BitLocker bez key readiness.
- **STOP:** błędy RAM.
- **STOP:** nieustalony OS volume.
- **STOP:** firmware nie widzi dysku.

Jeżeli wystąpi flaga, zatrzymaj testy, zabezpiecz dowody i przejdź do eskalacji. Nie interpretuj
braku telemetrii jako potwierdzenia zdrowia.

## Zgodność

Obsługuj Windows XP SP3–11, ale przed komendą sprawdź build, edition, x86/x64/ARM64, język,
online/Safe Mode/WinRE/WinPE/offline oraz BIOS/MBR albo UEFI/GPT. Najpierw otwórz
[references/compatibility.md](references/compatibility.md), gdy środowisko jest legacy, offline,
ARM64, w trybie S, N, LTSC/LTSB lub zarządzane. W WinRE nigdy nie zakładaj `C:`.

## Drzewo objaw → dowód → hipoteza → test

1. **Objaw:** WinRE uruchamia się przy każdym starcie. → **hipoteza:** Pending update, driver, component corruption albo storage. → **test:** Najpierw layout/storage, potem zebrać SrtTrail i pending state. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.
2. **Objaw:** Kursor jest, system odpowiada. → **hipoteza:** Explorer, display driver, profile lub shell extension. → **test:** Sprawdzić Ctrl+Shift+Esc, Safe Mode i zdalny event timeline. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.
3. **Objaw:** Logo pojawia się, potem reset. → **hipoteza:** Bugcheck ukryty przez auto-restart, driver, RAM/storage. → **test:** Wyłączyć auto-restart wyłącznie w WinRE menu, zebrać bugcheck/dump. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.

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

- `Boot layout` — WinRE — PowerShell/CMD, R0; szczegóły w [references/command-cards.md](references/command-cards.md#boot-layout).
- `SrtTrail` — WinRE — Command Prompt, R0; szczegóły w [references/command-cards.md](references/command-cards.md#srttrail).
- `Boot entries` — WinRE/Windows — CMD jako administrator, R0; szczegóły w [references/command-cards.md](references/command-cards.md#boot-entries).

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

- [`windows-bcd-partition-repair`](../windows-bcd-partition-repair/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`winpe-offline-repair`](../winpe-offline-repair/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`storage-triage-cloning-recovery`](../storage-triage-cloning-recovery/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`windows-bsod-debugging`](../windows-bsod-debugging/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.

## Źródła

- `ms-startup-repair` — [Startup Repair](https://support.microsoft.com/en-us/windows/startup-repair-85deb0b9-fa3d-44d8-a2d1-2a6aee1f1e94) (zweryfikowano 2026-08-06).
- `ms-bcdedit` — [BCDEdit command-line options](https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/bcdedit--set) (zweryfikowano 2026-08-06).
- `ms-winre` — [Windows Recovery Environment](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-recovery-environment--windows-re--technical-reference) (zweryfikowano 2026-08-06).

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
