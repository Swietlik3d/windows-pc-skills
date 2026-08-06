---
name: windows-ntfs-permissions-shares
description: "Prowadzi bezpieczną diagnostykę i kontrolowane działania dla: precyzyjną diagnozę ownership, dziedziczenia, effective access, share ACL, offline ACL i świadomość EFS. Aktywuj przy zgłoszeniach: Access denied; NTFS permissions; SMB share permission; toegang geweigerd. Use for Windows service diagnostics in this domain; do not use outside this scope. Zawsze zaczynaj od ochrony danych i dowodów."
---

# NTFS ACL i udziały SMB

## Cel i granice odpowiedzialności

Prowadź precyzyjną diagnozę ownership, dziedziczenia, effective access, share ACL, offline ACL i świadomość EFS. Rozdzielaj fakty, hipotezy, testy i wyniki. Nie wykonuj zmian bez
autoryzacji odpowiedniej do R0–R4. Nie wykonywać masowego takeown/icacls reset na dysku systemowym.

## Kiedy aktywować i kiedy nie aktywować

Aktywuj dla fraz: `Access denied`, `NTFS permissions`, `SMB share permission`, `toegang geweigerd`. Nie aktywuj dla
problemów, których główna przyczyna należy do powiązanego skilla; router wybiera dokładnie jeden
skill główny. Użytkowanie jawne `$$windows-ntfs-permissions-shares` ma pierwszeństwo, ale nie znosi bramek bezpieczeństwa.

## Dane wejściowe i minimalne pytania bezpieczeństwa

Najpierw ustal: czy system startuje; czy istnieje zweryfikowany backup; czy dane są cenniejsze niż
urządzenie; czy BitLocker/Device Encryption jest włączony; czy urządzenie jest domain/Entra/MDM;
jakie były ostatnie zmiany; jaki dokładnie objaw i czas reprodukcji. Nie pytaj o recovery key,
hasło, token ani pełny product key. Dla tej domeny zbierz:

- identity/SID.
- current ACL SDDL.
- inheritance.
- share permissions.
- effective access.
- EFS status.

## Szybki triage i czerwone flagi

- **STOP:** EFS encrypted files.
- **STOP:** organizacyjny share.
- **STOP:** nieznany właściciel danych.
- **STOP:** root system drive target.
- **STOP:** brak ACL backup.

Jeżeli wystąpi flaga, zatrzymaj testy, zabezpiecz dowody i przejdź do eskalacji. Nie interpretuj
braku telemetrii jako potwierdzenia zdrowia.

## Zgodność

Obsługuj Windows XP SP3–11, ale przed komendą sprawdź build, edition, x86/x64/ARM64, język,
online/Safe Mode/WinRE/WinPE/offline oraz BIOS/MBR albo UEFI/GPT. Najpierw otwórz
[references/compatibility.md](references/compatibility.md), gdy środowisko jest legacy, offline,
ARM64, w trybie S, N, LTSC/LTSB lub zarządzane. W WinRE nigdy nie zakładaj `C:`.

## Drzewo objaw → dowód → hipoteza → test

1. **Objaw:** Właściciel ma upoważnienie. → **hipoteza:** Explicit deny, orphan SID lub share ACL. → **test:** Eksport icacls i porównanie NTFS/share effective path. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.
2. **Objaw:** Foldery pokazują unknown account. → **hipoteza:** ACL odwołują się do starego SID. → **test:** Mapować stare/nowe konto i EFS przed zmianą. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.
3. **Objaw:** NTFS lokalnie OK. → **hipoteza:** Share ACL, SMB auth, firewall lub network profile. → **test:** Sprawdzić Get-SmbShareAccess i test z autoryzowanego klienta. → **przejście:** naprawiaj dopiero po uzyskaniu dowodu.

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

- `ACL odczyt` — Windows — PowerShell 5.1, R0; szczegóły w [references/command-cards.md](references/command-cards.md#acl-odczyt).
- `ACL backup` — Windows — CMD jako administrator, R1; szczegóły w [references/command-cards.md](references/command-cards.md#acl-backup).
- `Share ACL` — Windows — PowerShell jako administrator, R0; szczegóły w [references/command-cards.md](references/command-cards.md#share-acl).

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

- [`windows-accounts-profiles`](../windows-accounts-profiles/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`windows-network-repair`](../windows-network-repair/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`windows-bitlocker-tpm-security`](../windows-bitlocker-tpm-security/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.
- [`windows-case-evidence`](../windows-case-evidence/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę.

## Źródła

- `ms-icacls` — [icacls](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls) (zweryfikowano 2026-08-06).
- `ms-smbshare` — [SmbShare module](https://learn.microsoft.com/en-us/powershell/module/smbshare/) (zweryfikowano 2026-08-06).
- `ms-efs` — [Encrypting File System](https://learn.microsoft.com/en-us/windows/win32/fileio/file-encryption) (zweryfikowano 2026-08-06).

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
