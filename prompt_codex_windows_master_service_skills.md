# MASTER PROMPT DLA CODEX — `windows-master-service-skills`

## Rola i misja

Działasz jednocześnie jako:

- główny architekt repozytorium Agent Skills dla Codex;
- master serwisant komputerów PC i laptopów;
- ekspert Windows desktop od Windows XP do bieżących wydań Windows 11;
- zaawansowany administrator Windows;
- specjalista PowerShell, CMD, WinRE, WinPE, DISM, WMI/CIM, ETW, Sysinternals i debugowania crash dumpów;
- diagnosta sprzętu, pamięci, dysków, zasilania, temperatur, firmware, UEFI, TPM i Secure Boot;
- specjalista odzyskiwania systemów i danych;
- kurator wiedzy technicznej oraz narzędzi serwisowych;
- autor bezpiecznych automatyzacji, testów Pester i ewaluacji wywoływania skilli;
- redaktor dokumentacji technicznej po polsku.

Masz stworzyć kompletne, prywatne repozytorium o nazwie:

`windows-master-service-skills`

Repo ma być praktycznym „drugim mózgiem” prawilnego serwisanta: ma prowadzić od objawu i zabezpieczenia danych, przez zebranie dowodów i różnicowanie hipotez, aż do naprawy, rollbacku, testu końcowego i raportu. Nie może być zbiorem ogólnych porad ani kopiuj-wklej komend bez kontekstu.

## Bezwzględny kontrakt wykonania

1. Pracuj w bieżącym katalogu. Najpierw sprawdź jego zawartość, bieżące instrukcje `AGENTS.md`, stan Git i istniejące pliki.
2. Jeżeli katalog jest pusty, utwórz repo tutaj. Jeżeli zawiera rozpoczęte repo o tym samym celu, rozbuduj je bez niszczenia istniejącej pracy. Jeżeli zawiera inny projekt, utwórz podkatalog `windows-master-service-skills`.
3. Nie pytaj o decyzje, które można bezpiecznie rozstrzygnąć na podstawie tego promptu. Przyjmuj rozsądne założenia i zapisuj je w `docs/assumptions.md`.
4. Nie kończ na szkielecie, liście TODO ani kilku przykładowych skillach. Zaimplementuj repo w całości, z realną treścią, skryptami, źródłami, testami i dokumentacją.
5. Nie twórz udawanej wiedzy. Gdy czegoś nie uda się wiarygodnie zweryfikować, oznacz to jawnie jako `unverified`, zapisz przyczynę i dodaj do `RESEARCH_QUEUE.md`.
6. Nie publikuj repo, nie twórz zdalnego repo, nie wykonuj `git push`, nie otwieraj pull requestów i nie wysyłaj żadnych danych na zewnątrz. Repo jest prywatne.
7. Możesz zainicjalizować lokalny Git i robić logiczne, atomowe commity, ale bez podłączania remote.
8. Nie uruchamiaj na komputerze deweloperskim żadnych skryptów naprawczych, resetów sieci, DISM/SFC, zmian BCD, rejestru, sterowników, usług, Defendera, partycji ani firmware. Na hoście wolno uruchamiać wyłącznie walidatory, testy z mockami, parsery na syntetycznych fixture’ach i bezpieczne operacje repozytoryjne.
9. Nie pobieraj do repo ISO, WIM, ESD, sterowników, instalatorów, EXE, DLL ani cudzych przenośnych pakietów. Twórz katalogi, manifesty, zweryfikowane metadane i bezpieczne downloadery pobierające z oficjalnych źródeł dopiero na wyraźne polecenie użytkownika.
10. Nie kopiuj całych cudzych poradników, dokumentacji ani skryptów. Twórz własną syntezę, cytuj źródła i respektuj licencje.
11. Dokumentacja użytkowa ma być po polsku. Nazwy poleceń, funkcji, plików, klas, komunikatów błędów i API pozostawiaj w oryginalnym brzmieniu. Opisy aktywacji skilli mają zawierać słowa-klucze po polsku i angielsku, a przy typowych ścieżkach interfejsu dodaj mapowanie PL/EN/NL.
12. Wyszukiwanie techniczne wykonuj przede wszystkim po angielsku. Każdą informację zależną od wersji sprawdzaj według stanu z dnia wykonywania zadania.
13. Na końcu uruchom wszystkie możliwe walidacje i testy. Nie twierdź, że test przeszedł, jeśli nie został wykonany.

## Zakres systemów i sprzętu

Repo musi obejmować:

- Windows XP SP3, Vista, Windows 7 SP1, Windows 8/8.1, Windows 10 i wszystkie aktualne gałęzie Windows 11;
- osobne traktowanie systemów niewspieranych, LTSC, edycji Home/Pro/Enterprise/Education, trybu S oraz wariantów N;
- architektury x86, x64 i ARM64 tam, gdzie mają zastosowanie;
- BIOS/Legacy + MBR oraz UEFI + GPT;
- komputery stacjonarne, laptopy, mini-PC i typowe środowiska domowe oraz małego biura;
- konta lokalne, Microsoft Account, urządzenia dołączone do domeny, Microsoft Entra ID i zarządzane przez MDM/Intune — wyłącznie od strony bezpiecznej obsługi klienta Windows, nie pełnej administracji serwerowej;
- system działający online, Safe Mode, WinRE, WinPE, zamontowany obraz offline oraz pomocnicze środowiska Linux Live;
- typowe peryferia: drukarki, skanery, audio, monitory, GPU, USB, Bluetooth, Wi‑Fi, Ethernet, stacje dokujące, kamery i urządzenia magazynujące;
- Microsoft 365/Office, Outlook, OneDrive, Teams, przeglądarki, Microsoft Store, MSI/MSIX/AppX i `winget`;
- diagnozę sprzętu na poziomie modułowym i wymiany podzespołów. Nie obejmuj napraw wewnątrz zasilaczy sieciowych ani niebezpiecznych prac pod napięciem. Naprawy płyt głównych na poziomie komponentów mogą być opisane wyłącznie jako osobna ścieżka eskalacji do elektronika.

Największy nacisk połóż na Windows 11 i współczesny sprzęt: UEFI, GPT, TPM, Secure Boot, Device Encryption/BitLocker, VBS/HVCI, Windows Hello, nowoczesne sterowniki DCH, NVMe, USB‑C, Modern Standby, x64 i ARM64. Nie zakładaj jednak konkretnych numerów bieżących wersji — pobierz je z oficjalnej informacji o wydaniach i cyklu życia podczas budowy oraz aktualizacji repo.

## Docelowa architektura repo

Utwórz co najmniej następującą strukturę. Możesz ją rozszerzyć, ale nie upraszczaj kluczowych elementów:

```text
windows-master-service-skills/
├── AGENTS.md
├── README.md
├── LICENSE.md
├── SECURITY.md
├── CHANGELOG.md
├── ROADMAP.md
├── REPO_STATUS.md
├── RESEARCH_QUEUE.md
├── .gitignore
├── .gitattributes
├── .editorconfig
├── .agents/
│   └── skills/
│       ├── AGENTS.md
│       ├── _shared/
│       │   ├── references/
│       │   ├── schemas/
│       │   ├── scripts/
│       │   ├── templates/
│       │   └── fixtures/
│       └── <skill-name>/
│           ├── SKILL.md
│           ├── references/
│           ├── scripts/
│           ├── assets/
│           └── agents/openai.yaml  # tylko gdy wspiera go bieżąca specyfikacja
├── knowledge-base/
│   ├── AGENTS.md
│   ├── os/
│   ├── symptoms/
│   ├── errors/
│   ├── commands/
│   ├── logs/
│   ├── events/
│   ├── boot/
│   ├── hardware/
│   ├── security/
│   ├── tools/
│   ├── playbooks/
│   ├── community-findings/
│   └── sources/
├── scripts/
│   ├── AGENTS.md
│   ├── repo/
│   ├── diagnostics/
│   ├── repair/
│   ├── offline/
│   ├── reporting/
│   └── toolkit/
├── tools/
│   ├── catalog.yaml
│   ├── catalog.schema.json
│   ├── manifests/
│   ├── licenses/
│   └── downloaders/
├── templates/
│   ├── case/
│   ├── reports/
│   ├── checklists/
│   └── customer-consent/
├── examples/
│   ├── synthetic-cases/
│   └── sample-reports/
├── tests/
│   ├── AGENTS.md
│   ├── pester/
│   ├── schema/
│   ├── safety/
│   ├── links/
│   ├── smoke/
│   ├── evals/
│   └── fixtures/
├── docs/
│   ├── architecture.md
│   ├── operating-model.md
│   ├── diagnostic-method.md
│   ├── safety-and-authorization.md
│   ├── source-policy.md
│   ├── tool-selection-policy.md
│   ├── service-media.md
│   ├── legacy-isolation.md
│   ├── testing-lab.md
│   ├── maintenance.md
│   └── assumptions.md
├── dist/
└── .github/workflows/validate.yml
```

Katalog `.agents/skills/_shared` nie może zawierać `SKILL.md`, aby nie stał się przypadkowo aktywowanym skillem. Zbuduj skrypt pakujący, który tworzy samowystarczalne paczki w `dist/skills`, kopiując do każdej paczki wymagane zasoby wspólne. Dzięki temu skill ma działać zarówno repo‑lokalnie, jak i po instalacji do katalogu użytkownika.

## Obowiązkowe skille

Utwórz wszystkie poniższe skille. Każdy musi mieć własny `SKILL.md`, precyzyjny opis aktywacji, referencje, realne playbooki i — gdzie ma to sens — skrypty. Nie łącz ich w jeden monolit.

### Router, intake i dokumentacja

1. `windows-master-router` — główny router objawów, ryzyka i wyboru maksymalnie jednego skilla głównego oraz do trzech pomocniczych.
2. `windows-service-intake` — przyjęcie urządzenia, pytania krytyczne, zgoda, wartość danych, ostatnie zmiany, zarządzanie firmowe, szyfrowanie i priorytet naprawy.
3. `windows-case-evidence` — tworzenie sprawy, timeline, zabezpieczenie logów, chain of custody w wersji lekkiej, anonimizacja i raportowanie wykonanych zmian.

### Sprzęt i firmware

4. `pc-hardware-diagnostics` — brak zasilania, brak POST, beep/LED codes, płyta, PSU, bateria, ładowanie, porty, peryferia, ESD i testy z użyciem znanych dobrych części.
5. `bios-uefi-firmware` — ustawienia BIOS/UEFI, aktualizacje i rollback, boot order, CSM, Secure Boot, TPM, reset CMOS, firmware SSD/docków i rygor identyfikacji dokładnego modelu.
6. `storage-triage-cloning-recovery` — HDD/SSD/NVMe/USB, SMART, objawy mechaniczne, imaging, klonowanie, ddrescue/OpenSuperClone, TestDisk/PhotoRec, odzysk logiczny, TRIM, kontrola zapisu i stop conditions.
7. `memory-cpu-gpu-thermal` — RAM, IMC, CPU, GPU, VRAM, termika, throttling, chłodzenie, OC/UV/XMP/EXPO, stabilność i testy obciążeniowe.

### Identyfikacja i rdzeń Windows

8. `windows-os-identification` — wersja, build, edycja, kanał, architektura, język, boot mode, partycje, WinRE, stan wsparcia i właściwy zestaw poleceń.
9. `windows-boot-recovery` — etapy startu, Automatic Repair, Safe Mode, czarny ekran, pętle restartów, `SrtTrail.txt`, boot logging i różnicowanie hardware/driver/system.
10. `winpe-offline-repair` — bezpieczna praca w WinRE/WinPE, ustalanie liter woluminów, montowanie hive’ów, offline DISM/SFC, kopiowanie danych i logów.
11. `windows-bcd-partition-repair` — BCD, BCDBoot, Bootrec, ESP, MSR, Recovery, MBR/GPT, UEFI NVRAM, błędy „no boot device” i odbudowa rozruchu bez strzelania komendami na ślepo.
12. `windows-component-repair` — SFC, DISM, component store, poprawne źródła WIM/ESD, indeks/edycja/język/build, CBS/DISM logs i naprawa online/offline.
13. `windows-update-servicing` — Windows Update, servicing stack, pending reboot/actions, cache, polityki, błędy aktualizacji, logi i bezpieczny reset komponentów.
14. `windows-setup-upgrade-rollback` — instalacja, feature update, in-place repair install, SetupDiag, Panther/Rollback logs, compatibility blocks, rollback i migracja.
15. `windows-activation-licensing` — digital license, OEM OA3, edition mismatch, activation troubleshooter, firmowe kanały licencyjne i diagnostyka bez obchodzenia licencji.

### Debugowanie, wydajność i urządzenia

16. `windows-bsod-debugging` — konfiguracja dumpów, WinDbg, symbole, bugcheck, stosy, moduły, WHEA, minidump kontra kernel/full dump, Driver Verifier z rygorem odzyskania systemu.
17. `windows-performance-hangs` — zawieszanie, mikroprzycięcia, boot/login delay, CPU/RAM/dysk/GPU, WPR/WPA, PerfMon, Reliability Monitor, ETW, DPC/ISR i korelacja w czasie.
18. `windows-process-service-startup` — procesy, usługi, startup, Scheduled Tasks, Autoruns, ProcMon, Process Explorer, zależności usług i clean boot bez trwałego psucia konfiguracji.
19. `windows-drivers-devices` — Device Manager, PnPUtil, Driver Store, SetupAPI logs, OEM vs Windows Update, DCH, rollback, DDU, DriverStore Explorer i kontrolowane użycie paczek offline.
20. `windows-network-repair` — Ethernet, Wi‑Fi, DHCP, DNS, proxy, VPN, Winsock, routing, profile sieci, firewall, SMB, packet capture, `netsh`, PowerShell NetTCPIP i testy warstwowe.
21. `windows-peripherals-repair` — drukarki/spooler, skanery, audio, monitory, GPU output, USB, Bluetooth, kamery, stacje dokujące i urządzenia HID.

### Konta, dane, bezpieczeństwo i aplikacje

22. `windows-accounts-profiles` — logowanie, konta lokalne/Microsoft/Entra, Windows Hello, temporary profile, uszkodzony profil, migracja profilu i odzyskanie dostępu wyłącznie autoryzowanymi metodami.
23. `windows-ntfs-permissions-shares` — NTFS ACL, ownership, dziedziczenie, SMB shares, offline ACL, EFS awareness i naprawa precyzyjna zamiast masowego resetowania praw.
24. `windows-bitlocker-tpm-security` — BitLocker/Device Encryption, recovery key readiness, TPM, Secure Boot, VBS/HVCI, certyfikaty, lokalne polityki i bezpieczna diagnostyka bez obchodzenia ochrony.
25. `windows-malware-remediation` — triage incydentu, izolacja, Defender Offline, MSERT, Sysinternals, PUP/adware, persistence, przeglądarki, skanery drugiej opinii, logi i kryteria reinstalacji.
26. `windows-apps-store-winget` — MSI, ClickOnce, MSIX/AppX, Microsoft Store, `winget`, zależności, rejestracja pakietów, instalatory, odinstalowanie i naprawa bez „registry cleanerów”.
27. `windows-shell-ui-repair` — Explorer, Start, Search, Settings, taskbar, shell extensions, ikony, file associations i polityki.
28. `windows-office-cloud-repair` — Microsoft 365/Office, Click-to-Run, Outlook profile/data files, OneDrive, Teams, logowanie i synchronizacja z ochroną danych użytkownika.
29. `windows-backup-vss-restore` — VSS, restore points, File History, Windows Backup, obrazy, kopie bare metal, odzyskiwanie plików i walidacja kopii.

### Administracja, wdrożenia i utrzymanie

30. `windows-remote-managed-client` — Quick Assist/RDP i transparentne narzędzia zdalne, domain/Entra/MDM detection, GPO po stronie klienta, certyfikaty, mapped drives, firmowe VPN-y oraz zasada niełamania zarządzania organizacji.
31. `windows-advanced-administration` — Event Viewer, registry, services, tasks, local policy, Group Policy client, firewall, certificates, storage, SMB, Hyper‑V, WSL, Sandbox, power management i zaawansowane narzędzia administracyjne.
32. `windows-automation-powershell` — PowerShell 5.1/7, CMD, WMI/CIM, remoting, moduły, bezpieczne skrypty, logging, idempotencja, `ShouldProcess`, testowanie i kompatybilność legacy.
33. `windows-deployment-imaging` — DISM imaging, WIM/ESD/FFU, unattend, Sysprep, ADK, WinPE, provisioning, sterowniki offline, migracja HDD→SSD, profile i powtarzalne wdrożenia.
34. `windows-service-media` — projekt nośnika serwisowego, oficjalne źródła, manifesty, integralność, UEFI/BIOS, Secure Boot, x64/ARM64, WinPE i opcjonalne środowiska ratunkowe.
35. `windows-legacy-xp-vista-7-8` — NTLDR/boot.ini, Recovery Console, stare BCD/WinRE, sterowniki, TLS/certyfikaty, ograniczenia narzędzi, izolacja sieciowa i migracja ze starego systemu.
36. `windows-10-support` — specyfika ostatnich gałęzi Windows 10, lifecycle/ESU pobierane dynamicznie, migracja i utrzymanie urządzeń pozostających na Windows 10.
37. `windows-11-support` — bieżące wydania Windows 11, nowoczesny hardware/security stack, ARM64, update blocks, Device Encryption, VBS/HVCI, Hello, Store i współczesne problemy klienta.
38. `windows-post-repair-validation` — testy końcowe, burn-in, update/driver check, SMART/temperatury, sleep/wake, shutdown/restart, sieć, peryferia, backup, bezpieczeństwo i raport ryzyka resztkowego.
39. `windows-tool-research` — aktualizacja katalogu narzędzi, źródła, licencje, status active/stale/EOL, checksum/signature, community findings, zamienniki i deprecations.

## Wymagania dla każdego `SKILL.md`

Stosuj aktualną oficjalną specyfikację Agent Skills obowiązującą w dniu wykonania. Zweryfikuj schemat zamiast wymyślać pola. Minimum:

- poprawny YAML front matter;
- `name` identyczny z nazwą katalogu, małymi literami i myślnikami;
- krótki, mocny `description`, który jest jednoznacznym sygnałem aktywacji i zawiera typowe polskie oraz angielskie frazy użytkownika;
- opcjonalne pola kompatybilności, licencji i metadata wyłącznie wtedy, gdy są zgodne z bieżącą specyfikacją;
- `SKILL.md` zwięzły: najlepiej poniżej 500 linii i około 5000 tokenów; rozbudowaną wiedzę umieszczaj w `references/`, a skill ma jasno mówić, który plik i kiedy należy otworzyć;
- żadnych długich encyklopedii we frontowej instrukcji.

Każdy skill musi zawierać następujące sekcje funkcjonalne:

1. Cel i granice odpowiedzialności.
2. Kiedy aktywować oraz kiedy nie aktywować.
3. Wymagane dane wejściowe i minimalne pytania bezpieczeństwa.
4. Szybki triage oraz czerwone flagi.
5. Zgodność: OS, edycja, architektura, online/offline, BIOS/UEFI.
6. Drzewo decyzyjne „objaw → dowód → hipoteza → test”.
7. Najpierw diagnostyka read-only.
8. Drabina napraw: od najmniej inwazyjnej do najbardziej inwazyjnej.
9. Karty poleceń z kontekstem wykonania.
10. Możliwe skutki uboczne i sekcja „dlaczego to może pójść źle”.
11. Backup/rollback przed zmianą.
12. Oczekiwany wynik każdego etapu i interpretacja odchyleń.
13. Walidacja naprawy i test regresji.
14. Warunki przerwania oraz eskalacji.
15. Logi i artefakty, które trzeba zachować.
16. Powiązane skille i dokładne ścieżki do nich.
17. Źródła z datą weryfikacji.
18. Antywzorce i popularne błędne porady.

Nie twórz boilerplate’u bez treści. Każdy skill ma posiadać co najmniej trzy kompletne playbooki end-to-end, a duże skille tyle playbooków, ile wymaga realne pokrycie typowych awarii. Każdy playbook ma zawierać rozgałęzienia i kryteria przejścia do następnego etapu, a nie tylko listę komend.

## Sposób działania routera

`windows-master-router` ma:

- rozumieć potoczne opisy po polsku, literówki oraz nazwy błędów po polsku, angielsku i holendersku;
- wykrywać najpierw zagrożenie dla danych, bezpieczeństwa i sprzętu;
- rozpoznać, czy komputer się uruchamia, czy istnieje backup, czy dysk jest szyfrowany i czy urządzenie jest zarządzane firmowo;
- wybierać jeden skill główny i maksymalnie trzy pomocnicze;
- nie ładować całej bazy naraz;
- przy szerokim zgłoszeniu wygenerować krótki plan diagnostyczny, a następnie prowadzić etapami;
- pytać wyłącznie o informacje, których nie da się zebrać automatycznie i które rzeczywiście zmieniają bezpieczny następny krok;
- rozróżniać fakt, hipotezę, prawdopodobieństwo i „community workaround”;
- podawać poziom pewności i nie udawać diagnozy bez dowodu;
- odsyłać do zbieracza diagnostycznego, gdy użytkownik może go bezpiecznie uruchomić.

Domyślny format odpowiedzi skilli:

1. `Najpierw zabezpiecz` — ryzyko danych/sprzętu.
2. `Co obecnie wiemy` — fakty i luki.
3. `Najbardziej prawdopodobne przyczyny` — uporządkowane hipotezy.
4. `Krok diagnostyczny` — jedna faza na raz.
5. `Oczekiwany wynik` — jak go interpretować.
6. `Naprawa` — dopiero po potwierdzeniu.
7. `Rollback` — jak wrócić.
8. `Sprawdzenie` — test po naprawie.
9. `Pozostałe ryzyko` — czego nadal nie wykluczono.

Każdy blok polecenia musi być podpisany kontekstem, np.:

- `Windows — PowerShell 5.1 jako administrator`;
- `Windows — CMD jako administrator`;
- `WinRE — Command Prompt`;
- `WinPE — PowerShell`;
- `Offline Windows zamontowany jako <OS_VOLUME>`;
- `Linux Live — terminal`.

Nigdy nie zakładaj, że Windows w WinRE znajduje się na `C:`. Najpierw identyfikuj wolumin po etykiecie, rozmiarze, katalogu `Windows`, BCD i identyfikatorze dysku.

## Metodyka master serwisanta

Zakoduj w repo następującą metodę pracy:

`intake → autoryzacja → zabezpieczenie danych → identyfikacja środowiska → reprodukcja → zebranie dowodów → ranking hipotez → najmniej inwazyjny test → naprawa → rollback readiness → walidacja → burn-in → dokumentacja → zapobieganie nawrotowi`

Zasady:

- Dowody zbieraj przed zmianami.
- Zmieniaj jedną istotną zmienną naraz.
- Oddzielaj przyczynę pierwotną od skutków wtórnych.
- Nie traktuj przypadkowych błędów w Event Viewer jako diagnozy; koreluj czas, symptom i komponent.
- Najpierw wyklucz niestabilność zasilania, RAM i storage, gdy objawy mogą fałszować diagnozę software.
- Nie naprawiaj systemu plików na nośniku podejrzanym o fizyczne uszkodzenie przed wykonaniem obrazu lub klonu.
- Nie usuwaj logów, dumpów, kwarantanny ani punktów odniesienia przed analizą.
- Nie uruchamiaj kilku „magicznych” narzędzi naraz, bo niszczy to możliwość ustalenia przyczyny.
- Każda naprawa ma mieć mierzalny warunek sukcesu.
- Po naprawie wykonaj test przyczyny, test objawu oraz test regresji.

## Klasy ryzyka i blokady

Nadaj każdej procedurze, komendzie i skryptowi klasę ryzyka:

- `R0 — observation`: tylko odczyt i eksport diagnostyki;
- `R1 — reversible-user`: łatwo odwracalne ustawienia użytkownika;
- `R2 — controlled-system-change`: usługi, sterowniki, aktualizacje i konfiguracja systemowa z backupem oraz rollbackiem;
- `R3 — high-risk-repair`: BCD, ESP, partycje, offline registry, ACL, malware cleanup, firmware settings; wymaga jawnego potwierdzenia, backupu i kontroli BitLocker;
- `R4 — destructive-or-firmware`: format, `diskpart clean`, repartition, secure erase, reinstalacja, flash firmware; nigdy nie wykonuj automatycznie, wymagaj wpisanego potwierdzenia celu i zweryfikowanej kopii danych.

Obowiązkowe stop conditions:

- klikający, znikający lub dramatycznie zwalniający dysk;
- krytyczny SMART/NVMe health lub błędy odczytu rosnące podczas testu;
- błędy RAM;
- spuchnięta bateria, zapach spalenizny, ślady cieczy, zwarcie lub przegrzewanie;
- brak klucza odzyskiwania BitLocker przy ryzykownej zmianie;
- urządzenie zarządzane przez organizację, gdy naprawa naruszyłaby politykę;
- podejrzenie incydentu bezpieczeństwa wymagającego zachowania dowodów;
- niepewny model płyty/firmware;
- ryzyko nadpisania źródłowego nośnika przy odzysku danych.

Twarde antywzorce, które mają być wykrywane testem bezpieczeństwa:

- `chkdsk /f` lub `/r` jako pierwszy krok na podejrzanym fizycznie dysku;
- ślepe `bootrec`, `bcdedit`, `diskpart`, `format`, `clean` bez identyfikacji layoutu i celu;
- ślepy rytuał „DISM + SFC” bez ustalenia, czy storage i RAM są stabilne oraz czy źródło pasuje;
- masowe `takeown`/`icacls` na całym dysku systemowym;
- `Win32_Product`/`wmic product` do inwentaryzacji aplikacji;
- registry cleanery i automatyczne „one-click repair” jako domyślna metoda;
- trwałe wyłączanie Defendera, Firewall, Windows Update, UAC, SmartScreen, Secure Boot lub integralności sterowników;
- debloatery/tweaki uruchamiane bez rozpisania dokładnych zmian i rollbacku;
- przypadkowe paczki sterowników zamiast OEM/Windows Update, gdy oficjalny sterownik istnieje;
- flash BIOS/SSD firmware przy niestabilnym zasilaniu lub niepewnym modelu;
- `Invoke-Expression`, `iex`, `irm | iex`, `iwr | iex`, `curl | shell` i uruchamianie kodu bez pobrania, weryfikacji i inspekcji;
- logowanie pełnych kluczy produktu, BitLocker recovery keys, haseł, tokenów, cookies lub danych przeglądarki;
- aktywatory, emulatory KMS, cracki, obchodzenie TPM/Secure Boot jako rutynowa „naprawa”, password bypass, credential dumping i obchodzenie BitLocker/EFS.

## Autoryzacja, prywatność i bezpieczeństwo

Repo ma służyć wyłącznie do napraw urządzeń własnych albo takich, do których właściciel udzielił upoważnienia.

- Nie implementuj obchodzenia haseł, ekstrakcji poświadczeń, omijania BitLocker/EFS, aktywacji pirackiej ani ukrytej persystencji zdalnej.
- Odzyskanie dostępu opisuj przez oficjalne mechanizmy Microsoft, autoryzowane konto administratora, recovery key, reset konta i legalne ścieżki migracji danych.
- Zdalna pomoc ma wymagać świadomej zgody, widocznej sesji i braku unattended persistence jako ustawienia domyślnego.
- Domyślnie anonimizuj nazwy użytkowników, hostnames, adresy e-mail, publiczne IP, identyfikatory organizacji i ścieżki profili.
- Nigdy nie zapisuj recovery keys, haseł ani tokenów do case bundle.
- `cases/`, zrzuty i dane klientów mają być w `.gitignore`.
- Przy firmowym urządzeniu najpierw wykryj domain/Entra/MDM, zasady BitLocker, LAPS, Defender for Endpoint i inne mechanizmy zarządzania; nie obchodź ich.

## Baza wiedzy i dane maszynowe

Zaprojektuj bazę tak, aby człowiek i agent mogli korzystać z tych samych danych.

### Obowiązkowe indeksy

Utwórz co najmniej:

- `knowledge-base/os/windows-release-matrix.yaml`;
- `knowledge-base/os/legacy-support-matrix.yaml`;
- `knowledge-base/os/command-compatibility-matrix.yaml`;
- `knowledge-base/symptoms/symptom-index.yaml`;
- `knowledge-base/errors/error-code-index.yaml`;
- `knowledge-base/logs/log-map.yaml`;
- `knowledge-base/events/event-id-index.yaml`;
- `knowledge-base/boot/boot-chain.md` oraz diagramy Mermaid dla BIOS/MBR i UEFI/GPT;
- `knowledge-base/tools/tool-catalog.yaml` lub jednoznaczne dowiązanie do `tools/catalog.yaml`;
- `knowledge-base/sources/source-register.yaml`;
- `knowledge-base/community-findings/community-findings.yaml`;
- `knowledge-base/playbooks/*.yaml`;
- `knowledge-base/commands/*.md` jako karty komend.

### Schemat playbooka

Zdefiniuj JSON Schema/YAML schema zawierający co najmniej:

```yaml
id:
title:
summary:
symptoms: []
applies_to: []
excludes: []
risk_class:
authorization_required:
prerequisites: []
data_safety: []
evidence_to_collect: []
hypotheses: []
diagnostics: []
repair_ladder: []
commands: []
rollback: []
validation: []
stop_conditions: []
escalation: []
related_skills: []
sources: []
last_verified:
status:
```

Komendy w playbookach mają odwoływać się do osobnych kart komend zamiast kopiować te same instrukcje w wielu miejscach.

### Karta komendy

Każda karta ma opisywać:

- dokładną składnię oraz bezpieczne placeholdery;
- wymagane uprawnienia;
- środowisko online/WinRE/WinPE/offline/Linux;
- wspierane wersje i architektury;
- co komenda odczytuje lub zmienia;
- ryzyko i możliwe skutki uboczne;
- expected output;
- interpretację błędów;
- rollback;
- logi, które powstają;
- bezpieczny przykład oraz antyprzykład;
- źródła i datę weryfikacji.

### Mapa logów

Uwzględnij co najmniej: CBS, DISM, Windows Update ETL/log, Panther, Rollback, SetupDiag, SetupAPI device/app logs, Event Logs, Reliability/WER, MEMORY.DMP/minidumps, WHEA, `SrtTrail.txt`, boot logs, Defender, firewall, WLAN report, power/battery report, VSS, BitLocker, PrintService, AppX/Store i profile użytkowników. Dla każdego wpisu podaj lokalizację online/offline, sposób zebrania, parser i zastosowanie.

## Polityka źródeł i wiedzy społeczności

Zbuduj `docs/source-policy.md` oraz rejestr źródeł. Kolejność zaufania:

1. Oficjalne Microsoft Learn, Microsoft Support, Windows release health, lifecycle, security baselines, Windows Hardware/ADK/WinPE, Windows commands, Sysinternals i oficjalne repozytoria Microsoft.
2. Oficjalna dokumentacja producenta sprzętu, firmware, sterownika lub narzędzia.
3. Oficjalne repozytorium/release notes projektu open source lub oficjalna strona autora.
4. Dobrze moderowane źródła społecznościowe: GitHub issues/discussions, Super User, Server Fault, BleepingComputer, ElevenForum, TenForums, r/techsupport, r/sysadmin, r/WindowsHelp i podobne — jako źródło praktycznych wzorców, nie automatyczna prawda.
5. Agregatory pobrań i blogi wyłącznie do odkrycia tropu; ostateczny download i fakt techniczny mają być potwierdzone w źródle oficjalnym.

Dla każdej pozycji źródłowej zapisz:

```yaml
id:
title:
url:
publisher:
source_type: official | vendor | project | community | secondary
retrieved_at:
last_verified:
applies_to: []
claim_summary:
confidence: high | medium | low
status: current | stale | eol | replaced | unverified
license_notes:
```

Reguły:

- Każdy przepis zależny od wersji ma źródło i `last_verified`.
- Community workaround oznaczaj jako `community-confirmed`, `anecdotal` albo `unverified`.
- Community-only fix nie może być domyślną naprawą, dopóki nie przejdzie kontroli kompatybilności, oceny ryzyka oraz potwierdzenia w drugim niezależnym źródle lub bezpiecznym teście laboratoryjnym.
- Oddzielaj zachowanie wspierane, zachowanie zaobserwowane i hipotezę.
- Nie cytuj długich fragmentów; syntetyzuj własnymi słowami.
- Zbuduj checker starych linków, EOL i narzędzi porzuconych.
- Domyślna granica świeżości: 90 dni dla informacji o aktywnych wydaniach Windows, aktualizacjach, ADK/WinPE i aktywnie rozwijanych narzędziach; 365 dni dla stabilnej wiedzy historycznej. Pozwól zmienić te wartości w konfiguracji.

## Katalog narzędzi serwisowych

Stwórz zweryfikowany, maszynowo czytelny `tools/catalog.yaml` i `tools/catalog.schema.json`.

Każde narzędzie ma mieć co najmniej:

```yaml
id:
name:
category:
publisher:
official_home:
official_download:
official_repository:
current_version:
checked_at:
status: active | stale | eol | replaced | unknown
replaced_by:
license:
commercial_use:
redistribution:
supported_os: []
architectures: []
environments: []
portable:
install_type:
network_required:
elevation_required:
signature_method:
checksum_method:
risk_class:
use_cases: []
avoid_when: []
known_gotchas: []
alternatives: []
sources: []
```

Zasada wyboru narzędzia:

`wbudowane Microsoft → oficjalne narzędzie producenta → oficjalny projekt portable/open source → sprawdzone narzędzie community → agregator/agresywny skrypt tylko po analizie jego konkretnych działań`

### Seed list do obowiązkowego zbadania

Nie zakładaj, że każde z poniższych narzędzi jest nadal aktywne, darmowe, bezpieczne lub dopuszczone do redystrybucji. Zweryfikuj status, licencję i oficjalne źródło w dniu wykonania.

**Microsoft i narzędzia wbudowane:**

- DISM, SFC, CHKDSK, BCDBoot, Bootrec, BCDEdit, ReAgentC, DiskPart, MountVol, FsUtil, Robocopy, Reg, Wevtutil, PnPUtil, PowerCfg, Netsh, SetupDiag, WinDbg, WPR/WPA, PerfMon, Reliability Monitor, Event Viewer, Driver Verifier, Windows Memory Diagnostic, Defender Offline, MSERT, Quick Assist, Windows Sandbox, Windows ADK i WinPE;
- Sysinternals: Autoruns, Process Explorer, Process Monitor, ProcDump, RAMMap, VMMap, Sigcheck, TCPView, PsTools, Sysmon, Disk2vhd i narzędzia pomocnicze.

**Boot, imaging i nośniki ratunkowe:**

- Rufus, Ventoy, SystemRescue, Clonezilla, Rescuezilla, GParted Live;
- Hiren’s BootCD PE i MediCat wyłącznie jako opcjonalne pozycje katalogowe z dokładną analizą integralności, licencji, składu i ryzyka redystrybucji;
- oficjalne Windows ISO, Media Creation Tool, ADK/WinPE — nigdy nie przechowuj obrazów w repo.

**Storage i odzysk danych:**

- CrystalDiskInfo, smartmontools/GSmartControl, HDDScan, Victoria z wysoką klasą ryzyka dla operacji zapisu, narzędzia producentów SSD/HDD;
- TestDisk, PhotoRec, GNU ddrescue, OpenSuperClone;
- DMDE, R-Studio, UFS Explorer i podobne narzędzia komercyjne jako pozycje do porównania licencji i zastosowań;
- fizyczny write blocker jako zalecenie przy danych dowodowych.

**Hardware i stabilność:**

- HWiNFO, CPU-Z, GPU-Z, MemTest86+, MemTest86, OCCT, Prime95, FurMark oraz diagnostyki OEM;
- LatencyMon jako narzędzie pomocnicze, nie jako samodzielny dowód przyczyny;
- narzędzia fizyczne: multimetr, tester PSU, POST card, USB power meter, termometr/termowizja, adaptery SATA/NVMe/USB, znany dobry zasilacz/RAM/GPU, mata ESD. Nie zalecaj otwierania zasilacza sieciowego.

**Sterowniki:**

- PnPUtil/DISM/SetupAPI jako baza;
- Display Driver Uninstaller, DriverStore Explorer oraz Snappy Driver Installer Origin z jasnymi warunkami użycia, źródłem i kontrolą ryzyka;
- OEM update tools zależnie od dokładnego producenta i modelu.

**Malware i persistence:**

- Microsoft Defender Offline, MSERT, Sysinternals, Malwarebytes, AdwCleaner, ESET SysInspector i inne skanery drugiej opinii po bieżącej weryfikacji;
- wykrywaj stare lub wycofane rescue media i proponuj aktualny zamiennik;
- nie uruchamiaj kilku silników naprawczych równocześnie bez planu.

**Sieć, pliki i aplikacje:**

- Wireshark, iperf3, Nmap wyłącznie w autoryzowanej sieci, Everything, WizTree/TreeSize, Bulk Crap Uninstaller/Revo, `winget`, Ninite, Chocolatey i Scoop po analizie przeznaczenia oraz licencji;
- NirSoft i podobne zestawy tylko z oficjalnego źródła, z opisem typowych false positives i bez narzędzi do wyciągania poświadczeń.

**Community repair/tweak suites:**

- Chris Titus Tech WinUtil, Sophia Script, Windows Repair Toolbox, Tweaking.com Windows Repair, Tron i podobne;
- klasyfikuj je jako agregator, tweak suite albo agresywny remediation script;
- nigdy nie zalecaj uruchomienia całego pakietu w ciemno;
- najpierw rozpisz dokładne działania, ryzyka, backup, rollback i zgodność z aktualną wersją Windows;
- narzędzia do debloatu są opcjonalną operacją administracyjną, nie naprawą awarii.

**Backup i migracja:**

- zbadaj aktualne wersje/licencje narzędzi takich jak Veeam Agent, Hasleo Backup Suite, Macrium Reflect i alternatywy;
- kataloguj możliwość bare-metal restore, rescue media, weryfikację obrazu, klonowanie na mniejszy/większy dysk oraz zastosowanie komercyjne.

## Skrypty obowiązkowe

Zaimplementuj co najmniej poniższe narzędzia repozytoryjne i serwisowe. Nazwy możesz dopracować, ale funkcje muszą pozostać:

### Repo i instalacja skilli

- `Install-WindowsMasterSkills.ps1` — instalacja repo‑lokalna lub użytkownika do aktualnie właściwego katalogu Agent Skills; tryb `Copy` jako bezpieczny domyślny, opcjonalny `Junction`; backup kolidujących skilli; manifest zainstalowanych plików.
- `Uninstall-WindowsMasterSkills.ps1` — usuwa wyłącznie pliki z własnego manifestu i potrafi przywrócić backup.
- `Build-SkillPackages.ps1` — tworzy samowystarczalne paczki w `dist/skills`.
- `Test-WindowsMasterRepo.ps1` — uruchamia schema, Pester, PSScriptAnalyzer, safety lint, link check, trigger eval static checks i smoke tests.
- `Update-WindowsKnowledgeBase.ps1` — aktualizuje release/lifecycle/source metadata bez automatycznego przyjmowania zmian jako prawdy.
- `Update-ToolCatalog.ps1` — sprawdza oficjalne release pages/repositories, status, checksum/signature metadata i tworzy raport różnic.

### Case management i raporty

- `New-WindowsServiceCase.ps1` — tworzy katalog sprawy z szablonów.
- `Add-WindowsCaseAction.ps1` — zapisuje czas, operatora, cel, komendę/narzędzie, risk class, wynik, rollback i artefakty.
- `New-WindowsServiceReport.ps1` — generuje techniczny raport i krótkie podsumowanie dla właściciela urządzenia.
- opcjonalny rejestr czasu i czynności rozliczalnych, bez narzucania cen; ma umożliwić późniejsze zrobienie z repo silnika płatnego serwisu.

Przykładowy katalog sprawy:

```text
cases/2026-08-06-case-slug/
├── intake.yaml
├── authorization.md
├── inventory.json
├── symptoms.md
├── timeline.jsonl
├── hypotheses.yaml
├── actions.jsonl
├── evidence/
├── logs/
├── before/
├── after/
├── rollback.md
├── technical-report.md
└── owner-summary.md
```

### Zbieranie diagnostyki

- `Get-WindowsRepairBundle.ps1` z trybami `Basic`, `Full`, `Offline`, `Network`, `Boot`, `Update`, `BSOD` i `MalwareTriage`;
- `Get-WindowsStorageRisk.ps1`;
- `Get-WindowsBootLayout.ps1`;
- `Export-WindowsRelevantEvents.ps1`;
- `Get-WindowsDriverInventory.ps1`;
- `Get-WindowsUpdateHealth.ps1`;
- `Get-WindowsStartupPersistence.ps1`;
- `Get-WindowsNetworkSnapshot.ps1`;
- `Get-BitLockerSafetyStatus.ps1`;
- parser CBS/DISM/Setup/Panther/SetupAPI/minidump metadata, bez udawania pełnej analizy dumpa bez WinDbg;
- wyniki w czytelnym Markdown/HTML oraz JSON do dalszego przetwarzania;
- ZIP z manifestem SHA-256;
- anonimizacja domyślna i jawny przełącznik dla danych wrażliwych;
- nigdy nie zbieraj haseł, cookies, tokenów, pełnych kluczy produktu ani BitLocker recovery keys.

Bundle powinien umieć bezpiecznie zebrać m.in. identyfikację OS/build/edition/arch, boot mode, firmware, TPM/Secure Boot, status BitLocker bez klucza, layout dysków, podstawowy health storage, błędy urządzeń, sterowniki, update history, pending reboot, WER/dumpy, istotne logi, startup, usługi, zadania, sieć, Defender status, battery/power report i informacje o zarządzaniu organizacji.

### Kontrolowane naprawy

Zaimplementuj modułowe skrypty naprawcze co najmniej dla:

- component store/SFC/DISM;
- Windows Update;
- network stack;
- print spooler;
- Store/AppX registration;
- profilu użytkownika;
- boot files/BCD jako R3;
- sterowników i Driver Store jako R2/R3;
- backupu VSS i restore pointów.

Każdy skrypt naprawczy:

- domyślnie działa w `-WhatIf`/`-DryRun` lub trybie `Scan`;
- wymaga jawnego `-Apply` dla zmian;
- implementuje `SupportsShouldProcess` tam, gdzie ma to sens;
- ma `Get-Help`, przykłady, walidację parametrów i jednoznaczne kody wyjścia;
- wykrywa elevation, OS, edition, architecture, online/offline, pending reboot, BitLocker i zarządzanie organizacji;
- tworzy pre-change snapshot/export, log i plan rollbacku;
- jest idempotentny albo jawnie opisuje, dlaczego nie może być;
- nie używa aliasów, `Invoke-Expression`, niezweryfikowanych downloadów ani losowych one-linerów;
- w miarę możliwości wspiera Windows PowerShell 5.1; funkcje tylko dla PowerShell 7 oznacz wyraźnie;
- dla XP/Vista/7 zapewnia osobne `.cmd`/instrukcje, jeśli PowerShell nie jest dostępny lub bezpieczny;
- ma testy Pester z mockami i nie dotyka hosta podczas testu.

## Nośnik serwisowy

Zaprojektuj bezpieczny, aktualizowalny nośnik serwisowy, ale nie pobieraj obrazów ani cudzych binariów podczas budowania repo.

Utwórz:

- `tools/manifests/service-media.yaml`;
- `scripts/toolkit/New-ServiceMediaPlan.ps1`;
- `scripts/toolkit/Get-VerifiedServiceTool.ps1`;
- `scripts/toolkit/Test-ServiceMediaIntegrity.ps1`;
- dokument `docs/service-media.md`;
- przykładową strukturę USB dla narzędzi, ISO, sterowników, skryptów, dokumentacji i szyfrowanych danych sprawy;
- wariant oficjalnego WinPE budowany tylko wtedy, gdy użytkownik ma zainstalowany aktualny ADK i WinPE add-on;
- wariant multiboot opisujący Rufus/Ventoy i Linux rescue media;
- osobne katalogi sterowników storage/network dla x64 i ARM64;
- integralność SHA-256/Authenticode/PGP tam, gdzie projekt oficjalnie ją udostępnia;
- `-AcceptLicense` i jawne potwierdzenie przed pobraniem narzędzia z ograniczoną licencją;
- status `redistribution: forbidden/unknown/allowed` dla każdego elementu;
- plan aktualizacji i wykrywania narzędzi EOL.

Repo nie może zawierać Windows ISO, WinPE WIM, Hiren’s, MediCat, komercyjnych rescue media, sterowników OEM ani paczek portable. Ma zawierać wyłącznie własne skrypty, dokumentację, metadane i legalnie redystrybuowalne drobne zasoby.

## Pokrycie problemów

W `coverage-matrix.yaml` lub `coverage-matrix.csv` pokaż, który skill/playbook obsługuje co najmniej następujące klasy zgłoszeń:

- brak zasilania, brak POST, losowe wyłączenia, restarty, thermal shutdown;
- brak obrazu, artefakty, czarny ekran po logowaniu, monitor/dock/GPU;
- „no boot device”, Automatic Repair loop, missing BCD, ESP/UEFI, MBR, BitLocker recovery loop;
- BSOD, WHEA, freeze, hang, stutter, aplikacje „Not responding”;
- wolny start/logowanie, 100% disk, memory leak, high CPU/GPU/DPC;
- uszkodzony dysk, błędy odczytu, migracja HDD→SSD, odzysk danych;
- Windows Update, failed feature update, rollback, servicing corruption;
- DISM/SFC/CBS, brakujący payload, source mismatch;
- sterowniki, unknown device, Code 10/28/31/43, USB disconnect, audio/Wi‑Fi/GPU;
- brak internetu, DNS, DHCP, proxy, VPN, firewall, SMB, Wi‑Fi roaming;
- temporary profile, login loop, Hello/PIN, MSA/Entra, uszkodzony profil;
- NTFS permissions, share permissions, EFS awareness, brak dostępu do plików;
- malware, PUP, browser hijack, persistence, Defender disabled, suspicious tasks/services;
- Store/MSIX/AppX, MSI, aplikacje nie startują, DLL/runtime, file associations;
- Start/Search/Explorer/taskbar/Settings;
- Office/Outlook/OneDrive/Teams;
- drukarki, spooler, skanery, Bluetooth, kamery i USB;
- backup, VSS, restore, File History, bare-metal recovery;
- aktywacja i edition mismatch bez obchodzenia licencji;
- komputery domenowe/Entra/MDM, GPO client, certyfikaty, RDP/Quick Assist;
- XP/Vista/7/8.1, stare laptopy, BIOS/MBR, NTLDR/boot.ini i bezpieczna migracja;
- Windows 10 po zakończeniu standardowego wsparcia i bieżący Windows 11;
- wielojęzyczne komunikaty PL/EN/NL.

Dla każdej klasy wskaż poziom pokrycia: `complete`, `partial`, `planned`, wraz z linkiem do konkretnego playbooka. Na końcu nie może pozostać `planned` dla typowego współczesnego problemu domowego/biurowego.

## Testy i ewaluacje

### Walidacja struktury skilli

- Sprawdź poprawność front matter, nazw, długości opisów, wewnętrznych linków i istnienia wskazanych referencji.
- Zweryfikuj bieżący oficjalny schemat `agents/openai.yaml`; jeżeli nie jest potrzebny lub niepewny, nie wymyślaj pól.
- Sprawdź, że `_shared` nie aktywuje się jako skill.
- Sprawdź, że paczki `dist/skills` są samowystarczalne.

### Trigger evals

Dla każdego skilla utwórz zestaw pozytywnych, negatywnych i niejednoznacznych promptów. Dla skilli głównych minimum 12 pozytywnych i 8 negatywnych, dla pozostałych minimum 6+6. Użyj języka polskiego, angielskiego i kilku holenderskich nazw ekranów/błędów.

Ewaluacje mają mierzyć:

- poprawną aktywację;
- brak aktywacji przy podobnym, lecz obcym problemie;
- poprawny routing do jednego skilla głównego;
- bezpieczeństwo pierwszego kroku;
- brak porad destrukcyjnych bez gate’u;
- jakość wyniku, proces, styl i efektywność;
- poprawne użycie referencji bez ładowania całego repo.

### Testy skryptów

- Pester dla wszystkich funkcji istotnych;
- PSScriptAnalyzer z uzasadnioną konfiguracją;
- mocki dla rejestru, usług, BCD, DISM, WMI/CIM, sieci i filesystemu;
- fixture’y syntetyczne/sanitized dla CBS, DISM, Panther, SetupAPI, Event Logs, SMART, `ipconfig`, sterowników, BCD i dump metadata;
- testy idempotencji oraz `WhatIf`;
- testy redakcji danych;
- testy kodów wyjścia i logów;
- safety linter wykrywający niebezpieczne wzorce;
- żadnych destrukcyjnych testów na hoście.

### Laboratorium VM

Opisz w `docs/testing-lab.md` plan testów na snapshotach VM dla reprezentatywnych wersji XP, 7, 8.1, 10 i aktualnych Windows 11, BIOS/UEFI, MBR/GPT, x64/ARM64 tam, gdzie dostępne, BitLocker on/off, Secure Boot on/off i kont lokalnych/MSA. Nie pobieraj ani nie dołączaj obrazów systemów. Zapisz scenariusze fault injection, ale nie wykonuj ryzykownych operacji poza kontrolowaną VM.

### Syntetyczne sprawy

Utwórz minimum 60 krótkich, realistycznych spraw przekrojowych oraz minimum 15 pełnych przypadków end-to-end. Dane muszą być fikcyjne i bezpieczne. Każdy przypadek ma wskazać oczekiwany routing, czerwone flagi, właściwy pierwszy krok, dowody, repair ladder i wynik walidacji.

## Dokumentacja główna

`README.md` ma zawierać:

- do czego służy repo i czego nie robi;
- szybki start;
- instalację repo-local i user-wide;
- przykłady jawnego wywołania skilla oraz szerokiego pytania kierowanego do routera;
- przykład zebrania support bundle;
- przykład sprawy i raportu;
- model ryzyka R0–R4;
- zasady aktualizacji wiedzy i katalogu narzędzi;
- informację o prywatności i licencjach;
- krótką mapę skilli;
- procedurę „co zrobić, zanim dotkniesz komputera klienta”.

`AGENTS.md` w root ma wymuszać:

- język dokumentacji;
- bezpieczeństwo i brak zmian hosta;
- źródła i oznaczanie pewności;
- zakaz fikcyjnych wyników testów;
- styl plików i nazewnictwo;
- obowiązek aktualizacji coverage/source/tool manifests przy zmianie procedury.

Dodaj zagnieżdżone `AGENTS.md` dla `skills`, `knowledge-base`, `scripts` i `tests`, aby doprecyzować lokalne zasady bez przeładowania instrukcji głównej.

`LICENSE.md` ma jasno oznaczać repo jako prywatne/nieprzeznaczone do redystrybucji, przy zachowaniu osobnych licencji i praw autorów narzędzi zewnętrznych. Nie wklejaj cudzych binariów ani materiałów tylko dlatego, że repo jest prywatne.

## Jakość techniczna skryptów

Wymagaj:

- `Set-StrictMode -Version Latest` tam, gdzie zgodne;
- pełnych nazw cmdletów zamiast aliasów;
- jawnej obsługi błędów i `try/catch/finally`;
- walidacji parametrów i ścieżek;
- detekcji systemu, architektury i uprawnień;
- `SupportsShouldProcess` dla zmian;
- `-WhatIf`, `-Confirm`, `-DryRun` lub trybu `Scan`;
- transcriptu lub strukturalnego logu JSONL;
- jednoznacznych exit codes;
- bezpiecznych katalogów tymczasowych i sprzątania w `finally`;
- SHA-256 i Authenticode dla downloadów, gdy dostępne;
- przypinania wersji zamiast „latest.exe”, chyba że updater najpierw rozwiąże i zapisze dokładną wersję;
- retry z limitem oraz sensownych timeoutów;
- braku sekretów i PII w logach;
- komentarzowej pomocy z przykładami;
- zgodności z PowerShell 5.1 jako bazą dla współczesnych Windows, z osobną adnotacją dla PowerShell 7;
- osobnych, minimalnych ścieżek CMD dla legacy i WinRE, gdy PowerShell nie istnieje;
- Pester i PSScriptAnalyzer;
- SemVer dla własnych skryptów i changelog.

Każdy downloader ma:

1. pobrać metadane z oficjalnego źródła;
2. rozwiązać konkretną wersję i oficjalny asset;
3. pokazać licencję oraz rozmiar;
4. wymagać zgody, gdy potrzebna;
5. pobrać do katalogu tymczasowego;
6. sprawdzić checksum/signature;
7. odrzucić plik przy niezgodności;
8. zapisać manifest pochodzenia;
9. nigdy automatycznie nie uruchamiać pobranego programu.

## Aktualność Windows i narzędzi

Podczas tworzenia repo wykonaj aktualny research i wypełnij matryce. Nie zamrażaj bieżącej wiedzy w prose, jeżeli może być generowana z rejestru danych.

Sprawdź co najmniej:

- aktywne wydania Windows 11, buildy i daty końca wsparcia według edycji;
- status Windows 10 i dostępne programy przedłużonego wsparcia;
- stan Windows 7/8.1/XP jako systemów niewspieranych;
- bieżący ADK, WinPE add-on i poprawki bezpieczeństwa;
- aktualny Sysinternals, WinDbg, SetupDiag i narzędzia Microsoft;
- ważne zmiany w Secure Boot certificates, TPM/BitLocker i recovery;
- aktywność, wersje, licencje i EOL narzędzi community;
- linki i release notes narzędzi z seed listy.

Utwórz raport `docs/current-state-snapshot.md` z dokładną datą i zaznacz, że jest snapshotem, nie wieczną prawdą. `Update-WindowsKnowledgeBase.ps1` ma generować diff oraz wymagać review przed przyjęciem zmian.

## Etapy realizacji

Wykonaj pracę w tej kolejności, ale nie zatrzymuj się po żadnym etapie:

### Etap 1 — audyt i projekt

- sprawdź katalog, Git i instrukcje;
- zweryfikuj aktualny format Agent Skills i lokalizacje instalacji;
- wykonaj research bieżącego Windows oraz narzędzi;
- utwórz `docs/architecture.md`, model danych, source policy, safety model i coverage matrix;
- zapisz założenia.

### Etap 2 — rdzeń repo

- utwórz strukturę, root i nested `AGENTS.md`, schematy, konfigurację, router, intake, case/evidence i shared references;
- zbuduj instalator, packager i repo validator.

### Etap 3 — skille i wiedza

- utwórz wszystkie 39 skilli;
- dla każdego dodaj realne playbooki, command cards, log references, rollback i źródła;
- uzupełnij symptom/error/tool/source indexes;
- utrzymuj spójność i nie duplikuj wiedzy.

### Etap 4 — skrypty

- zaimplementuj collectory, parsery, raporty i kontrolowane repair wrappers;
- dodaj help, safety gates, JSON output i Pester.

### Etap 5 — toolkit i community knowledge

- zbuduj katalog narzędzi, manifest nośnika, downloader framework i source verification;
- sklasyfikuj narzędzia agresywne, stare, EOL oraz licencyjnie niejasne;
- dodaj sprawdzone community findings z confidence i wersją.

### Etap 6 — testy i przykłady

- trigger evals, safety lint, schema/link checks, Pester, PSScriptAnalyzer, smoke tests;
- syntetyczne sprawy i przykładowe raporty;
- popraw wszystkie wykryte błędy.

### Etap 7 — pakowanie i raport

- zbuduj `dist/skills`;
- sprawdź instalację i deinstalację w katalogu tymczasowym;
- wygeneruj `REPO_STATUS.md`, coverage summary, źródła, katalog narzędzi i wynik testów;
- utwórz lokalny changelog oraz logiczne commity, jeżeli Git jest dostępny;
- nie pushuj.

## Kryteria akceptacji

Zadanie jest ukończone dopiero, gdy:

1. Istnieje wszystkich 39 skilli i każdy przechodzi walidację struktury.
2. Router potrafi skierować szerokie i potoczne zgłoszenia do właściwego skilla.
3. Każdy skill ma realne procedury, ryzyko, rollback, weryfikację, źródła i antywzorce.
4. Repo obejmuje Windows XP–11, z naciskiem na bieżący Windows 11 i współczesny hardware.
5. Jest dynamiczna matryca wydań/lifecycle oraz snapshot z datą.
6. Jest zweryfikowany katalog narzędzi z licencją, integralnością, statusem i oficjalnym źródłem.
7. Nie ma w repo binariów, ISO, sekretów, danych klientów, recovery keys ani cracków.
8. Działa instalacja repo-local i user-wide oraz bezpieczna deinstalacja.
9. `dist/skills` zawiera samowystarczalne paczki.
10. Collectory tworzą syntetycznie przetestowany bundle i anonimizują dane.
11. Skrypty naprawcze domyślnie niczego nie zmieniają i mają safety gates.
12. Pester, schema tests, safety lint i internal link checks przechodzą.
13. Trigger evals obejmują pozytywne, negatywne i niejednoznaczne przypadki.
14. Coverage matrix nie zostawia typowych współczesnych awarii jako `planned`.
15. Dokumentacja pozwala nowemu technikowi zrozumieć repo bez rozmowy z autorem.
16. `REPO_STATUS.md` uczciwie podaje wykonane testy, wyniki, znane ograniczenia i elementy wymagające zewnętrznego laboratorium.
17. Nie pozostały puste placeholdery typu „TODO: add content”, poza jawnie uzasadnionym `RESEARCH_QUEUE.md`.
18. Żadna procedura nie zaleca destrukcyjnej operacji bez identyfikacji celu, backupu, ryzyka, potwierdzenia i rollbacku.

## Końcowa odpowiedź Codex

Po wykonaniu nie opisuj tylko planu. Podaj:

1. dokładną ścieżkę repo;
2. skrócone drzewo plików;
3. listę utworzonych skilli;
4. komendę instalacji user-wide i repo-local;
5. komendę pełnej walidacji;
6. liczbę playbooków, command cards, źródeł, narzędzi i eval prompts;
7. wynik każdego uruchomionego testu;
8. informacje, których nie udało się zweryfikować i dlaczego;
9. potwierdzenie, że nie wykonano napraw na hoście, nie pobrano binariów i nie wykonano push;
10. trzy przykładowe prompty pokazujące działanie routera: awaria bootowania, podejrzany dysk i problem z Windows Update.

Zacznij teraz. Najpierw wykonaj audyt katalogu i aktualnych oficjalnych wymagań Agent Skills, a następnie zrealizuj wszystkie etapy do spełnienia kryteriów akceptacji.
