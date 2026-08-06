---
name: windows-setup-upgrade-rollback
description: "Prowadzi bezpieczną diagnostykę i kontrolowane działania dla: analizę in-place setup, feature update, compatibility blocks, SetupDiag, Panther/Rollback i kontrolowany rollback. Aktywuj przy zgłoszeniach: upgrade failed; SetupDiag; Windows installatie teruggedraaid; in-place repair install. Use for Windows service diagnostics in this domain; do not use outside this scope. Zawsze zaczynaj od ochrony danych i dowodów."
---

# Setup, upgrade i rollback

## Cel i granice odpowiedzialności

Prowadź analizę in-place setup, feature update, compatibility blocks, SetupDiag, Panther/Rollback i kontrolowany rollback. Rozdzielaj fakty, hipotezy, testy i wyniki. Nie wykonuj zmian bez
autoryzacji odpowiedniej do R0–R4. Nie używać do zwykłej comiesięcznej KB bez logów Setup/Panther.

## Kiedy aktywować i kiedy nie aktywować

Aktywuj dla fraz: `upgrade failed`, `SetupDiag`, `Windows installatie teruggedraaid`, `in-place repair install`. Nie aktywuj dla
problemów, których główna przyczyna należy do powiązanego skilla; router wybiera dokładnie jeden
skill główny. Użytkowanie jawne `$$windows-setup-upgrade-rollback` ma pierwszeństwo, ale nie znosi bramek bezpieczeństwa.

## Dane wejściowe i minimalne pytania bezpieczeństwa

Najpierw ustal: czy system startuje; czy istnieje zweryfikowany backup; czy dane są cenniejsze niż
urządzenie; czy BitLocker/Device Encryption jest włączony; czy urządzenie jest domain/Entra/MDM;
jakie były ostatnie zmiany; jaki dokładnie objaw i czas reprodukcji. Nie pytaj o recovery key,
hasło, token ani pełny product key. Dla tej domeny zbierz:

- SetupDiag result.
- Panther/Rollback logs.
- compat scan.
- build/edition/language.
- drivers/apps.
- free space.

## Szybki triage i czerwone flagi

- **STOP:** brak backupu.
- **STOP:** storage/RAM instability.
- **STOP:** BitLocker not ready.
- **STOP:** unsupported hardware bypass.
- **STOP:** managed safeguard hold.

Jeżeli wystąpi flaga, zatrzymaj testy, zabezpiecz dowody i przejdź do eskalacji. Nie interpretuj
braku telemetrii jako potwierdzenia zdrowia.

## Zgodność

Obsługuj Windows XP SP3–11, ale przed komendą sprawdź build, edition, x86/x64/ARM64, język,
online/Safe Mode/WinRE/WinPE/offline oraz BIOS/MBR albo UEFI/GPT. Najpierw otwórz
[references/compatibility.md](references/compatibility.md), gdy środowisko jest legacy, offline,
ARM64, w trybie S, N, LTSC/LTSB lub zarządzane. W WinRE nigdy nie zakładaj `C:`.

## Drzewo objaw → dowód → hipoteza → test

1. **Objaw:** Setup wraca do poprzedniego builda. → **hipoteza:** Rule match wskazuje driver/app/partition. → **test:** Uruchomić parser na kopii logów i potwierdzić fazę. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.
2. **Objaw:** System działa, component repair nie wystarcza. → **hipoteza:** Repair install może zachować apps/data, ale wymaga zgodnego media. → **test:** Sprawdzić edition/language/build, backup i BitLocker. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.
3. **Objaw:** Windows Update nie oferuje wersji. → **hipoteza:** Microsoft/OEM safeguard może być zamierzony. → **test:** Sprawdzić release health i SetupCompat logs. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.

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

- `Parse Panther` — Repo — PowerShell 5.1+, R0; szczegóły w [references/command-cards.md](references/command-cards.md#parse-panther).
- `SetupDiag` — Windows — CMD jako administrator, R0; szczegóły w [references/command-cards.md](references/command-cards.md#setupdiag).
- `Compatibility scan` — Windows — CMD jako administrator, R0; szczegóły w [references/command-cards.md](references/command-cards.md#compatibility-scan).

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

- [`windows-update-servicing`](../windows-update-servicing/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`windows-component-repair`](../windows-component-repair/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`windows-drivers-devices`](../windows-drivers-devices/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`windows-backup-vss-restore`](../windows-backup-vss-restore/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.

## Źródła

- `ms-setupdiag` — [SetupDiag](https://learn.microsoft.com/en-us/windows/deployment/upgrade/setupdiag) (zweryfikowano 2026-08-06).
- `ms-setup-logfiles` — [Windows Setup log files](https://learn.microsoft.com/en-us/windows/deployment/upgrade/log-files) (zweryfikowano 2026-08-06).
- `ms-release-health` — [Windows release health](https://learn.microsoft.com/en-us/windows/release-health/) (zweryfikowano 2026-08-06).

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
