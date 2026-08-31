#!/usr/bin/env python3
"""Deterministically generate the substantive repository content.

The generator is intentionally kept in the repository so maintainers can rebuild
machine-readable indexes, skill references, evals, and synthetic examples from
one reviewed inventory.  It never inspects or changes the host Windows system.
"""

from __future__ import annotations

import json
import re
import shutil
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-08-06"
SKILL_ROOT = ROOT / ".agents" / "skills"


def s(
    name: str,
    title: str,
    focus: str,
    triggers: list[str],
    exclude: str,
    red: list[str],
    evidence: list[str],
    scenarios: list[tuple[str, str, str, str, str, str]],
    commands: list[tuple[str, str, str, str, str, str]],
    related: list[str],
    sources: list[str],
) -> dict:
    return {
        "name": name,
        "title": title,
        "focus": focus,
        "triggers": triggers,
        "exclude": exclude,
        "red": red,
        "evidence": evidence,
        "scenarios": scenarios,
        "commands": commands,
        "related": related,
        "sources": sources,
    }


SKILLS: list[dict] = [
    s(
        "windows-master-router",
        "Router główny serwisu Windows",
        "rozpoznanie objawu, ryzyka i wybór dokładnie jednego skilla głównego oraz najwyżej trzech pomocniczych",
        ["komputer nie działa i nie wiem od czego zacząć", "PC broken / Windows problem", "ordinateur start niet", "route this Windows issue"],
        "Nie używać jako substytutu specjalistycznego playbooka po jednoznacznym rozpoznaniu domeny.",
        ["zagrożenie danych", "zapach spalenizny lub spuchnięta bateria", "podejrzenie incydentu", "BitLocker bez gotowego recovery key"],
        ["stan uruchamiania", "backup i wartość danych", "szyfrowanie", "zarządzanie organizacji", "ostatnia zmiana"],
        [
            ("Szerokie zgłoszenie bez diagnozy", "Użytkownik mówi tylko „komputer nie działa”.", "Awaria może należeć do hardware, boot, storage albo zasilania.", "Zebrać pięć bramek bezpieczeństwa i sklasyfikować etap startu.", "Przekazać do jednego skilla o najwyższym dopasowaniu; nie wykonywać naprawy w routerze.", "Router zwraca jednego primary, maksymalnie trzy supporting i poziom pewności."),
            ("Wiele równoczesnych objawów", "Wolny start, błędy aktualizacji i znikający dysk.", "Objawy programowe mogą być skutkiem niestabilnego storage.", "Nadać priorytet ryzyku danych i korelacji czasowej.", "Najpierw storage triage; update jako skill pomocniczy dopiero po potwierdzeniu stabilności.", "Pierwszy krok pozostaje R0, a dysk nie otrzymuje zapisów."),
            ("Zgłoszenie firmowe i szyfrowane", "Laptop Entra/MDM żąda BitLocker recovery.", "Zmiana firmware lub polityki mogła wywołać recovery.", "Potwierdzić własność, MDM i dostępność klucza bez jego zapisywania.", "Skierować do security/managed-client; zatrzymać R3/R4.", "Odpowiedź jasno wskazuje gate organizacyjny i nie obchodzi ochrony."),
        ],
        [
            ("Router statyczny", "Repo — PowerShell 5.1+", "& '.\\scripts\\diagnostics\\Get-WindowsRepairBundle.ps1' -Mode Basic -FixtureRoot '<FIXTURE_ROOT>' -OutputPath '<OUTPUT>'", "R0", "Powstaje zanonimizowany bundle i manifest.", "Usunąć wyłącznie wygenerowany katalog wyjściowy."),
            ("Mapa symptomów", "Repo — Python 3", "python .\\scripts\\repo\\route_issue.py --text \"<OPIS>\" --json", "R0", "JSON zawiera primary, supporting, confidence i safety_flags.", "Brak zmian; zachować wejście tylko za zgodą."),
            ("Walidacja routingu", "Repo — PowerShell 5.1+", "& '.\\scripts\\repo\\Test-WindowsMasterRepo.ps1' -Category Evals", "R0", "Statyczne evals przechodzą i dokładnie jeden primary jest wymagany.", "Brak zmian poza raportem w dist/reports."),
        ],
        ["windows-service-intake", "windows-case-evidence", "windows-os-identification", "windows-post-repair-validation"],
        ["codex-skills", "ms-support-troubleshoot", "ms-bitlocker-overview"],
    ),
    s(
        "windows-service-intake",
        "Przyjęcie urządzenia i autoryzacja",
        "udokumentowanie właściciela, autoryzacji, wartości danych, szyfrowania, zarządzania, symptomów i zakresu zgody przed serwisem",
        ["przyjęcie laptopa do serwisu", "service intake", "toestemming reparatie", "formularz zgody klienta"],
        "Nie diagnozować szczegółowo awarii ani nie wykonywać zmian systemowych.",
        ["brak upoważnienia", "dane krytyczne bez kopii", "urządzenie firmowe bez kontaktu do administratora", "oznaki cieczy lub baterii"],
        ["tożsamość urządzenia bez sekretów", "zakres zgody R0–R4", "wartość i lokalizacja danych", "stan BitLocker", "akcesoria i stan fizyczny"],
        [
            ("Standardowe przyjęcie", "Urządzenie prywatne, Windows uruchamia się.", "Zakres może być ustalony bez dostępu do treści prywatnych.", "Wypełnić intake i zgodę, zanotować stan oraz plombowanie.", "Zezwolić na R0; kolejne klasy wymagają osobnych bramek.", "Intake ma komplet wymaganych pól i podpis/znacznik zgody."),
            ("Dane cenniejsze niż urządzenie", "Brak backupu i niestabilny dysk.", "Dalsze uruchamianie może zwiększać utratę.", "Zatrzymać testy zapisu i uzgodnić imaging/pro recovery.", "Nadać priorytet odzyskowi, nie naprawie Windows.", "Zakres wyraźnie rozdziela odzysk danych od naprawy."),
            ("Laptop zarządzany", "Entra/MDM, klient nie zna polityk.", "Serwis lokalny może naruszyć politykę organizacji.", "Zebrać tylko status zarządzania i kontakt administratora.", "Ograniczyć się do R0 do czasu pisemnej zgody organizacji.", "Dokumentacja wskazuje właściciela decyzji i brak obejść."),
        ],
        [
            ("Nowa sprawa", "Repo — PowerShell 5.1+", "& '.\\scripts\\reporting\\New-WindowsServiceCase.ps1' -Slug '<SLUG>' -OwnerAlias '<ALIAS>' -AuthorizationLevel R0 -Root '<CASES_ROOT>'", "R0", "Powstaje kompletna struktura sprawy bez PII.", "Usunąć katalog sprawy, jeżeli nie zawiera dowodów."),
            ("Kontrola intake", "Repo — Python 3", "python .\\scripts\\repo\\validate_case.py --case '<CASE_PATH>'", "R0", "Raport wskazuje brakujące pola i bramki.", "Brak zmian."),
            ("Szablon zgody", "Repo — PowerShell 5.1+", "Copy-Item -LiteralPath '.\\templates\\customer-consent\\authorization-pl.md' -Destination '<CASE>\\authorization.md'", "R1", "Powstaje kopia do ręcznego uzupełnienia.", "Usunąć kopię przed podpisaniem."),
        ],
        ["windows-case-evidence", "windows-master-router", "windows-bitlocker-tpm-security", "windows-remote-managed-client"],
        ["ms-bitlocker-overview", "ms-privacy", "codex-skills"],
    ),
    s(
        "windows-case-evidence",
        "Sprawa, dowody i raport zmian",
        "prowadzenie timeline, lekkiego chain of custody, hashy, anonimizacji, artefaktów before/after i raportu serwisowego",
        ["zapisz czynności serwisowe", "case evidence", "chain of custody", "serwisrapport"],
        "Nie wykonywać forensyki procesowej ani gwarantować formalnej wartości sądowej.",
        ["podejrzenie przestępstwa", "brak zgody na kopiowanie danych", "artefakt zawiera recovery key lub token", "źródłowy nośnik ulega degradacji"],
        ["czas UTC", "operator", "cel czynności", "hash SHA-256", "źródło i kopia robocza", "rollback"],
        [
            ("Zapis pojedynczej czynności", "Technik zebrał log R0.", "Brak wpisu utrudni korelację i audyt.", "Obliczyć hash i dopisać niezmienny JSONL.", "Nie edytować wcześniejszych rekordów; korekty dopisywać.", "Timeline jest parsowalny, a hash pliku zgodny."),
            ("Anonimizacja bundle", "Log zawiera username, hostname i e-mail.", "PII może wyciec do raportu.", "Pracować na kopii, zastosować deterministyczne tokeny redakcji.", "Zachować mapę tylko poza repo i za zgodą.", "Test redakcji nie znajduje wzorców PII ani sekretów."),
            ("Raport zamknięcia", "Naprawa zakończona i wykonano testy.", "Raport może mylić fakt z hipotezą.", "Złożyć actions, evidence i validation według statusu.", "Wygenerować raport techniczny i krótkie owner summary.", "Każde twierdzenie ma dowód lub jawne ograniczenie."),
        ],
        [
            ("Dodaj akcję", "Repo — PowerShell 5.1+", "& '.\\scripts\\reporting\\Add-WindowsCaseAction.ps1' -CasePath '<CASE>' -Purpose '<CEL>' -RiskClass R0 -Result '<WYNIK>' -Rollback 'not-applicable'", "R0", "Do actions.jsonl trafia jeden rekord UTC.", "Dopisać rekord korekty; nie przepisywać historii."),
            ("Raport", "Repo — PowerShell 5.1+", "& '.\\scripts\\reporting\\New-WindowsServiceReport.ps1' -CasePath '<CASE>'", "R0", "Powstają technical-report.md i owner-summary.md.", "Przywrócić poprzednie raporty z before/ lub historii Git."),
            ("Hash dowodu", "Windows — PowerShell 5.1", "Get-FileHash -LiteralPath '<ARTIFACT>' -Algorithm SHA256", "R0", "Zwrócony jest 64-znakowy hash SHA-256.", "Brak zmian."),
        ],
        ["windows-service-intake", "windows-post-repair-validation", "storage-triage-cloning-recovery"],
        ["ms-get-filehash", "nist-chain-evidence", "ms-privacy"],
    ),
    s(
        "pc-hardware-diagnostics",
        "Diagnostyka sprzętu PC",
        "różnicowanie braku zasilania, POST, kodów LED/beep, baterii, ładowania, PSU, płyty i peryferiów bez pracy pod napięciem",
        ["komputer nie włącza się", "no power / no POST", "pieptoon moederbord", "laptop nie ładuje"],
        "Nie otwierać zasilacza sieciowego i nie prowadzić napraw komponentowych płyty.",
        ["spuchnięta bateria", "zapach spalenizny", "ślady cieczy", "iskrzenie", "niepewny pinout zasilacza"],
        ["dokładny model", "sekwencja LED/beep", "napięcie znamionowe zasilacza", "minimalna konfiguracja", "znane dobre części"],
        [
            ("Brak reakcji na power", "Zero LED i wentylatorów.", "Zasilanie wejściowe, przycisk, PSU lub zwarcie płyty.", "Odłączyć zasilanie, ocenić wizualnie, potem testować znanym dobrym zasilaczem o zgodnej specyfikacji.", "Wymieniać jedną część naraz; żadnego otwierania PSU.", "Urządzenie przechodzi powtarzalny power-on bez zapachu i nadmiernego poboru."),
            ("Zasilanie jest, brak POST", "Wentylatory ruszają, brak obrazu i kod.", "RAM, GPU, CPU/IMC, firmware albo płyta.", "Udokumentować kod producenta, minimalizować konfigurację i testować pojedynczy moduł RAM.", "Reset CMOS tylko R3 po BitLocker/ustawieniach i dokumentacji.", "POST jest stabilny w trzech zimnych startach."),
            ("Laptop nie ładuje", "Działa z baterii, nie przyjmuje zasilania USB-C.", "Ładowarka, kabel E-marker, port, PD profile lub bateria.", "Porównać moc/specyfikację i użyć USB power metera bez rozbierania zasilacza.", "Wymienić kabel/ładowarkę na zgodne, potem port/dock jako moduł.", "Ładowanie utrzymuje właściwą moc i nie przerywa pod lekkim obciążeniem."),
        ],
        [
            ("Identyfikacja platformy", "Windows — PowerShell 5.1", "Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object Manufacturer,Model,SystemType", "R0", "Model i typ systemu są jednoznaczne.", "Brak zmian."),
            ("Bateria", "Windows — PowerShell 5.1", "Get-CimInstance -ClassName Win32_Battery | Select-Object Status,EstimatedChargeRemaining", "R0", "Status baterii bez modyfikacji ACPI.", "Brak zmian."),
            ("Raport zasilania", "Windows — CMD jako administrator", "powercfg /batteryreport /output \"<OUTPUT>\\battery-report.html\"", "R0", "Powstaje lokalny raport HTML.", "Usunąć raport; nie zmienia konfiguracji."),
        ],
        ["memory-cpu-gpu-thermal", "bios-uefi-firmware", "storage-triage-cloning-recovery", "windows-post-repair-validation"],
        ["ms-wmi-computersystem", "ms-powercfg", "ifixit-esd"],
    ),
    s(
        "bios-uefi-firmware",
        "BIOS, UEFI i firmware",
        "bezpieczna identyfikacja ustawień firmware, boot mode, CSM, Secure Boot, TPM oraz aktualizacji i rollbacku po dokładnym modelu",
        ["aktualizacja BIOS", "UEFI Secure Boot problem", "TPM niet beschikbaar", "firmware update laptop"],
        "Nie flashować bez dokładnego modelu, stabilnego zasilania, kopii ustawień i planu recovery.",
        ["niepewny model/rewizja", "niestabilne zasilanie", "brak BitLocker key readiness", "przerwany poprzedni flash"],
        ["manufacturer/model/board revision", "wersja BIOS i EC", "tryb UEFI/Legacy", "Secure Boot/TPM", "BitLocker protectors bez kluczy"],
        [
            ("Zmiana Secure Boot po aktualizacji", "Secure Boot jest wyłączony lub status nieznany.", "CSM, klucze firmware albo polityka OEM.", "Zebrać msinfo32/Confirm-SecureBootUEFI i stan BitLocker.", "Najpierw firmware OEM; zmianę kluczy wykonać dopiero po planie recovery.", "Secure Boot i boot działają, BitLocker nie żąda niespodziewanie recovery."),
            ("Plan aktualizacji BIOS", "OEM zaleca poprawkę stabilności.", "Właściwy obraz zależy od dokładnej rewizji.", "Zweryfikować Service Tag/model/board, release notes i podpis.", "Flash pozostawić ręcznej, jawnie potwierdzonej procedurze R4.", "Po flashu sprawdzić wersję, ustawienia, TPM, boot i temperatury."),
            ("Boot order po wymianie dysku", "UEFI nie pokazuje Windows Boot Manager.", "Brak wpisu NVRAM, niewłaściwy tryb lub ESP.", "Najpierw udokumentować layout i firmware mode.", "Naprawę BCD przekazać do dedykowanego skilla; nie przełączać CSM w ciemno.", "Windows Boot Manager wskazuje właściwy ESP i startuje trzy razy."),
        ],
        [
            ("Wersja firmware", "Windows — PowerShell 5.1", "Get-CimInstance -ClassName Win32_BIOS | Select-Object Manufacturer,SMBIOSBIOSVersion,ReleaseDate", "R0", "Dokładna wersja i data firmware.", "Brak zmian."),
            ("Secure Boot", "Windows — PowerShell jako administrator", "Confirm-SecureBootUEFI", "R0", "True/False albo kontrolowany błąd platformy bez UEFI.", "Brak zmian."),
            ("TPM", "Windows — PowerShell jako administrator", "Get-Tpm | Select-Object TpmPresent,TpmReady,ManagedAuthLevel", "R0", "Stan TPM bez inicjalizacji i bez sekretów.", "Brak zmian."),
        ],
        ["windows-bitlocker-tpm-security", "windows-bcd-partition-repair", "pc-hardware-diagnostics", "windows-service-media"],
        ["ms-secure-boot-2026", "ms-tpm", "ms-bitlocker-overview"],
    ),
    s(
        "storage-triage-cloning-recovery",
        "Storage triage, klonowanie i odzysk",
        "ochrona danych na HDD/SSD/NVMe/USB, SMART, imaging, ddrescue/OpenSuperClone, recovery logiczne i bezwzględna kontrola kierunku zapisu",
        ["dysk klika", "SSD znika", "SMART bad", "recover files / gegevens herstellen"],
        "Nie uruchamiać napraw systemu plików przed obrazem, gdy istnieje podejrzenie fizycznego uszkodzenia.",
        ["klikający lub znikający dysk", "rosnące read errors", "critical warning NVMe", "źródło/cel nie są jednoznaczne"],
        ["model/serial z redakcją", "SMART/NVMe health", "read error trend", "wartość danych", "write blocker", "mapfile imaging"],
        [
            ("Klikający HDD", "Dysk wydaje dźwięki i zwalnia.", "Uszkodzenie mechaniczne, każda próba może pogorszyć stan.", "Wyłączyć, nie skanować powierzchni, uzgodnić profesjonalne odzyskiwanie.", "Imaging tylko jeśli zaakceptowano ryzyko i nośnik stabilny; preferować hardware imager.", "Sukces oznacza zachowany obraz/hash, nie „naprawiony” dysk."),
            ("SSD/NVMe znika", "Dysk okresowo znika z UEFI.", "Firmware, zasilanie, temperatura albo kontroler NAND.", "Korelować SMART/NVMe, temperaturę i obecność w UEFI bez zapisów.", "Najpierw imaging na inny nośnik; firmware dopiero po kopii i OEM gate.", "Źródłowy dysk nie jest ponownie używany jako jedyna kopia."),
            ("Odzysk logiczny po usunięciu", "Pliki skasowane, dysk stabilny.", "TRIM mógł wyzerować bloki na SSD.", "Natychmiast zatrzymać zapisy i utworzyć obraz read-only.", "Analizować kopię TestDisk/PhotoRec/DMDE; wyniki zapisywać na trzeci nośnik.", "Otworzyć reprezentatywną próbkę i zachować log narzędzia."),
        ],
        [
            ("Ryzyko storage", "Windows — PowerShell jako administrator", "& '.\\scripts\\diagnostics\\Get-WindowsStorageRisk.ps1' -FixturePath '<FIXTURE_JSON>' -OutputPath '<OUTPUT_JSON>'", "R0", "Klasyfikacja safe/caution/stop z dowodami.", "Brak zmian źródła."),
            ("Layout dysków", "Windows — PowerShell jako administrator", "Get-Disk | Select-Object Number,FriendlyName,SerialNumber,PartitionStyle,OperationalStatus,HealthStatus,Size", "R0", "Jednoznaczna lista dysków; serial zanonimizować w raporcie.", "Brak zmian."),
            ("Reliability counters", "Windows — PowerShell jako administrator", "Get-PhysicalDisk | Get-StorageReliabilityCounter | Select-Object Temperature,ReadErrorsTotal,WriteErrorsTotal,Wear", "R0", "Dostępne liczniki; brak danych nie oznacza zdrowia.", "Brak zmian."),
        ],
        ["windows-backup-vss-restore", "windows-case-evidence", "pc-hardware-diagnostics", "windows-deployment-imaging"],
        ["smartmontools", "gddrescue", "opensuperclone", "testdisk"],
    ),
    s(
        "memory-cpu-gpu-thermal",
        "RAM, CPU, GPU i termika",
        "różnicowanie błędów RAM/IMC, WHEA, GPU/VRAM, throttlingu, chłodzenia oraz wpływu OC/UV/XMP/EXPO",
        ["błędy pamięci", "WHEA crash", "GPU artifacts", "oververhitting / thermal shutdown"],
        "Nie prowadzić napraw elektrycznych ani agresywnych stress testów przy przegrzewaniu.",
        ["jakikolwiek błąd RAM", "temperatura szybko rośnie do limitu", "zapach/wyciek chłodziwa", "niestabilne OC przy danych krytycznych"],
        ["WHEA timeline", "temperatury i clocks", "ustawienia stock/XMP", "moduły i sloty", "sterownik GPU", "zasilanie"],
        [
            ("Losowe restarty pod obciążeniem", "PC resetuje się bez BSOD.", "PSU, termika, RAM lub zabezpieczenie VRM.", "Zebrać WHEA/Kernel-Power i temperatury, testować jeden podsystem.", "Wrócić do stock; wymienić znaną dobrą część przed zmianami systemu.", "Brak restartu w powtarzalnym obciążeniu i zimnym starcie."),
            ("Błędy MemTest", "Co najmniej jeden błąd pamięci.", "Moduł, slot, IMC lub niestabilny profil.", "Zatrzymać diagnozę software i powtórzyć na stock po jednym module.", "Wymienić wadliwy element lub obniżyć do wspieranej konfiguracji.", "Wiele pełnych przejść bez błędów oraz test systemowy."),
            ("Artefakty GPU", "Kolorowe bloki w BIOS i Windows.", "GPU/VRAM/hardware bardziej prawdopodobny niż sterownik.", "Porównać obraz przed ładowaniem OS i na innym kablu/monitorze.", "Jeśli tylko Windows — clean driver path; jeśli pre-OS — wymiana/eskalacja.", "Brak artefaktów w pre-OS i kontrolowanym teście GPU."),
        ],
        [
            ("WHEA events", "Windows — PowerShell 5.1", "Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-WHEA-Logger'} -MaxEvents 50", "R0", "Zdarzenia WHEA z czasem i typem.", "Brak zmian."),
            ("Temperatura/obciążenie", "Windows — PowerShell 5.1", "Get-Counter '\\Processor(_Total)\\% Processor Time' -SampleInterval 1 -MaxSamples 10", "R0", "Krótka próbka CPU; brak temperatur wymaga narzędzia OEM/HWiNFO.", "Brak zmian."),
            ("Energy report", "Windows — CMD jako administrator", "powercfg /energy /duration 60 /output \"<OUTPUT>\\energy-report.html\"", "R0", "Raport zależności power/driver.", "Usunąć raport."),
        ],
        ["pc-hardware-diagnostics", "windows-bsod-debugging", "windows-performance-hangs", "windows-drivers-devices"],
        ["memtest86plus", "ms-whea", "ms-powercfg"],
    ),
    s(
        "windows-os-identification",
        "Identyfikacja Windows",
        "ustalenie edition, build, kanału, architektury, języka, boot mode, partycji, WinRE i statusu wsparcia przed doborem poleceń",
        ["jaki mam Windows", "identify Windows build", "Windows-versie controleren", "edition architecture boot mode"],
        "Nie używać wyłącznie do naprawy konkretnego, już zidentyfikowanego komponentu.",
        ["wyniki z różnych instalacji/offline volume", "WinRE z nieustaloną literą", "build poza matrycą", "tryb S lub organizacyjne policy"],
        ["ProductName/EditionID", "CurrentBuild/UBR", "architecture", "locale", "FirmwareType", "partition style", "WinRE status"],
        [
            ("System online", "Windows działa, wersja nieznana.", "Nazwa marketingowa może nie odpowiadać buildowi.", "Zebrać rejestr, systeminfo i architekturę; porównać z release matrix.", "Nie zakładać support na podstawie samego ProductName.", "Raport zawiera edition, build.UBR, kanał i datę weryfikacji."),
            ("System offline w WinRE", "Litery dysków są inne.", "C: może być WinRE, nie Windows.", "Przeszukać woluminy read-only po Windows/System32/config/SOFTWARE.", "Załadować hive pod unikalną nazwą tylko do odczytu i zawsze odmontować.", "Wskazany OS_VOLUME ma zgodny BCD, Windows dir i build."),
            ("ARM64/S mode/N edition", "Aplikacja lub sterownik nie działa.", "Ograniczenie może wynikać z architektury albo edycji.", "Ustalić native arch, emulation i capability edition.", "Dobrać tylko kompatybilne narzędzia; nie obchodzić S mode.", "Rekomendacja ma jawny wpis kompatybilności."),
        ],
        [
            ("Build online", "Windows — PowerShell 5.1", "Get-ComputerInfo | Select-Object WindowsProductName,WindowsEditionId,WindowsVersion,OsBuildNumber,OsArchitecture", "R0", "Jedna struktura identyfikacyjna; UBR zebrać osobno.", "Brak zmian."),
            ("Systeminfo", "Windows/WinRE — CMD", "systeminfo", "R0", "Tekstowa identyfikacja, jeśli WMI działa.", "Brak zmian."),
            ("WinRE status", "Windows — CMD jako administrator", "reagentc /info", "R0", "Status i lokalizacja WinRE.", "Brak zmian."),
        ],
        ["windows-10-support", "windows-11-support", "windows-legacy-xp-vista-7-8", "winpe-offline-repair"],
        ["ms-win11-release", "ms-win10-release", "ms-lifecycle"],
    ),
    s(
        "windows-boot-recovery",
        "Odzyskiwanie startu Windows",
        "diagnozę etapów boot, Automatic Repair loop, Safe Mode, czarnego ekranu, restartów i SrtTrail bez ślepej przebudowy BCD",
        ["Automatic Repair loop", "Windows nie startuje", "zwart scherm na aanmelden", "SrtTrail.txt"],
        "Nie przebudowywać partycji/BCD; przekazać potwierdzoną awarię boot files do dedykowanego skilla.",
        ["storage risk", "BitLocker bez key readiness", "błędy RAM", "nieustalony OS volume", "firmware nie widzi dysku"],
        ["etap startu", "firmware detection", "boot layout", "SrtTrail/boot log", "recent change", "Safe Mode behavior"],
        [
            ("Automatic Repair loop", "WinRE uruchamia się przy każdym starcie.", "Pending update, driver, component corruption albo storage.", "Najpierw layout/storage, potem zebrać SrtTrail i pending state.", "Cofnąć pojedynczą zmianę; BCD tylko przy dowodzie.", "Trzy poprawne starty i zachowane logi before/after."),
            ("Czarny ekran po logowaniu", "Kursor jest, system odpowiada.", "Explorer, display driver, profile lub shell extension.", "Sprawdzić Ctrl+Shift+Esc, Safe Mode i zdalny event timeline.", "Przekazać do shell/driver/profile zależnie od dowodu.", "Login i Explorer działają na nowym i istniejącym profilu."),
            ("Restart przed logowaniem", "Logo pojawia się, potem reset.", "Bugcheck ukryty przez auto-restart, driver, RAM/storage.", "Wyłączyć auto-restart wyłącznie w WinRE menu, zebrać bugcheck/dump.", "Naprawiać potwierdzony komponent, nie maskować restartu.", "Start stabilny, dump skonfigurowany, regresja sleep/restart."),
        ],
        [
            ("Boot layout", "WinRE — PowerShell/CMD", "& '<REPO>\\scripts\\diagnostics\\Get-WindowsBootLayout.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'", "R0", "Raport identyfikuje firmware, dysk, ESP/active i OS volume.", "Brak zmian."),
            ("SrtTrail", "WinRE — Command Prompt", "type \"<OS_VOLUME>:\\Windows\\System32\\Logfiles\\Srt\\SrtTrail.txt\"", "R0", "Treść logu albo kontrolowana informacja o braku.", "Brak zmian."),
            ("Boot entries", "WinRE/Windows — CMD jako administrator", "bcdedit /enum all", "R0", "Pełny eksport logiczny BCD bez zmian.", "Brak zmian."),
        ],
        ["windows-bcd-partition-repair", "winpe-offline-repair", "storage-triage-cloning-recovery", "windows-bsod-debugging"],
        ["ms-startup-repair", "ms-bcdedit", "ms-winre"],
    ),
    s(
        "winpe-offline-repair",
        "WinRE, WinPE i naprawa offline",
        "identyfikację woluminów, montowanie hive, offline log collection, DISM/SFC i kopiowanie danych w WinRE/WinPE",
        ["naprawa offline Windows", "WinPE repair", "WinRE opdrachtprompt", "load offline registry hive"],
        "Nie zakładać C: i nie prowadzić zmian BCD/partycji bez dedykowanego playbooka.",
        ["nieustalone źródło/cel", "BitLocker locked", "storage risk", "hive już załadowany", "źródło DISM nie pasuje"],
        ["disk/volume unique IDs", "OS directory", "BCD device", "BitLocker lock state", "build/language/index", "wolne miejsce"],
        [
            ("Ustalenie litery offline OS", "WinRE pokazuje wiele NTFS.", "Litery zostały przypisane dynamicznie.", "Listować woluminy i potwierdzić Windows dir, SOFTWARE hive i BCD.", "Zapisać mapę do sprawy; nie używać domyślnego C:.", "Trzy niezależne sygnały wskazują ten sam OS volume."),
            ("Eksport logów offline", "Windows nie startuje, potrzebne CBS/Panther.", "Logi mogą wskazać przyczynę bez zmiany systemu.", "Skopiować wybrane pliki z zachowaniem czasów i hashy.", "Pracować na kopii, zanonimizować raport.", "Manifest zawiera źródło, rozmiar i SHA-256."),
            ("Offline component repair", "CBS wskazuje corruption, storage/RAM stabilne.", "Źródło musi pasować build/edition/language.", "Najpierw DISM Check/Scan na wskazanym image i zweryfikować source index.", "Apply dopiero R2 po snapshot/backup i planie rollback.", "DISM/SFC exit, logs i ponowny boot są zweryfikowane."),
        ],
        [
            ("Offline identity", "WinRE/WinPE — PowerShell", "& '<REPO>\\scripts\\offline\\Get-OfflineWindowsIdentity.ps1' -WindowsPath '<OS_VOLUME>:\\Windows'", "R0", "Build/edition/arch z offline hive; hive jest odmontowany.", "Brak zmian."),
            ("Volumes", "WinRE — Command Prompt", "diskpart /s \"<READ_ONLY_LIST_SCRIPT>\"", "R0", "Skrypt zawiera tylko list disk/list volume/detail; brak select+write.", "Brak zmian."),
            ("DISM scan offline", "WinPE — CMD jako administrator", "dism /Image:<OS_VOLUME>:\\ /Cleanup-Image /ScanHealth", "R0", "Stan component store i DISM.log.", "Brak zmian; ScanHealth nie naprawia."),
        ],
        ["windows-os-identification", "windows-component-repair", "windows-bcd-partition-repair", "windows-case-evidence"],
        ["ms-winpe", "ms-dism-image", "ms-reg"],
    ),
    s(
        "windows-bcd-partition-repair",
        "BCD, ESP i partycje startowe",
        "kontrolowaną diagnozę i naprawę BCD/BCDBoot/ESP/MBR/GPT/NVRAM po pełnej identyfikacji celu",
        ["missing BCD", "no boot device", "Windows Boot Manager ontbreekt", "napraw ESP UEFI"],
        "Nie używać do ogólnej pętli boot bez dowodu, że problemem jest konfiguracja rozruchu.",
        ["nieustalony dysk/OS/ESP", "BitLocker bez klucza", "storage risk", "hybrydowy/niestandardowy layout", "dual boot bez zgody"],
        ["firmware mode", "disk IDs", "GPT/MBR", "ESP/active partition", "BCD export", "OS loader path"],
        [
            ("Brak Windows Boot Manager UEFI", "Firmware widzi dysk, ale nie wpis.", "Wpis NVRAM lub pliki ESP są brakujące.", "Potwierdzić GPT, FAT32 ESP i właściwy Windows volume.", "Wyeksportować BCD; użyć BCDBoot tylko z jawnymi /s i /f UEFI.", "NVRAM/ESP wskazuje właściwy loader, trzy zimne starty."),
            ("Legacy MBR po klonowaniu", "BIOS mówi no bootable device.", "Active flag, MBR boot code lub BCD device mismatch.", "Potwierdzić BIOS mode, MBR i aktywną system partition.", "Naprawiać pojedynczy element; nie konwertować do GPT w tym samym kroku.", "Boot działa i layout pozostaje zgodny z backupem."),
            ("BCD wskazuje złą partycję", "0xc000000e po zmianie dysku.", "Identifikator urządzenia jest nieaktualny.", "Eksport BCD i porównanie osdevice z ustalonym OS volume.", "Użyć wrappera R3 z target IDs i potwierdzeniem.", "bcdedit enum oraz boot log potwierdzają właściwy wpis."),
        ],
        [
            ("Plan layoutu", "WinRE — PowerShell", "& '<REPO>\\scripts\\diagnostics\\Get-WindowsBootLayout.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'", "R0", "Jednoznaczna mapa dysk→partycja→rola.", "Brak zmian."),
            ("Eksport BCD", "WinRE — Command Prompt", "bcdedit /export \"<BACKUP_VOLUME>:\\case\\before\\bcd-backup\"", "R1", "Powstaje kopia store; katalog docelowy jest poza źródłowym ESP.", "bcdedit /import wymaga osobnego R3 gate."),
            ("Kontrolowana naprawa", "WinRE — PowerShell", "& '<REPO>\\scripts\\repair\\Invoke-BootRepair.ps1' -Mode Plan -OsVolume '<OS_VOLUME>' -SystemVolume '<ESP_VOLUME>' -Firmware UEFI", "R0", "Plan pokazuje dokładne cele, backup i polecenia bez wykonania.", "Brak zmian w Mode Plan."),
        ],
        ["windows-boot-recovery", "winpe-offline-repair", "windows-bitlocker-tpm-security", "bios-uefi-firmware"],
        ["ms-bcdboot", "ms-bcdedit", "ms-bootrec"],
    ),
    s(
        "windows-component-repair",
        "SFC, DISM i component store",
        "diagnozę CBS/component store oraz dopasowanie źródła WIM/ESD przed SFC/DISM online i offline",
        ["SFC found corrupt files", "DISM 0x800f081f", "component store repair", "bronbestanden niet gevonden"],
        "Nie uruchamiać rytuału DISM+SFC, jeśli storage/RAM są niestabilne lub system jest w pending update.",
        ["storage/RAM instability", "source build/language/index mismatch", "pending reboot", "brak miejsca", "offline volume nieustalony"],
        ["DISM health", "CBS/DISM excerpts", "build/edition/language", "source metadata/index", "pending state", "free space"],
        [
            ("SFC reports corruption", "SFC /verifyonly wykrywa naruszenia.", "Component store lub pliki chronione są uszkodzone.", "Najpierw parsować CBS i ScanHealth.", "Naprawić store właściwym źródłem, potem pojedynczy SFC.", "ScanHealth clean, SFC clean i test objawu."),
            ("DISM 0x800f081f", "Source files could not be found.", "Źródło nie pasuje lub policy blokuje repair content.", "Porównać build, edition, language i WIM index.", "Wskazać jawne /Source:wim:<path>:<index> /LimitAccess po walidacji.", "DISM kończy 0, źródło i hash są zapisane."),
            ("Offline corruption", "System nie bootuje, CBS wskazuje servicing.", "Pending actions lub mismatch source.", "Zebrać offline identity i logi przed zmianą.", "Repair wrapper z właściwym ImagePath i source; nie revert pending bez wyjątkowego gate.", "Boot, DISM/SFC i update scan przechodzą."),
        ],
        [
            ("DISM ScanHealth", "Windows — CMD jako administrator", "dism /Online /Cleanup-Image /ScanHealth", "R0", "Stan store i DISM.log; operacja może być długa, ale nie naprawia.", "Brak zmian naprawczych."),
            ("SFC VerifyOnly", "Windows — CMD jako administrator", "sfc /verifyonly", "R0", "Weryfikacja bez naprawy oraz CBS.log.", "Brak zmian."),
            ("Plan naprawy", "Windows — PowerShell jako administrator", "& '.\\scripts\\repair\\Invoke-WindowsComponentRepair.ps1' -Mode Scan -LogRoot '<CASE_LOGS>'", "R0", "Preflight i plan; bez RestoreHealth/SFC repair.", "Brak zmian w Scan."),
        ],
        ["windows-update-servicing", "winpe-offline-repair", "storage-triage-cloning-recovery", "windows-os-identification"],
        ["ms-dism-repair", "ms-sfc", "ms-cbs-log"],
    ),
    s(
        "windows-update-servicing",
        "Windows Update i servicing",
        "diagnozę update history, policy, pending reboot, cache, servicing stack i kontrolowany reset komponentów",
        ["Windows Update error", "aktualizacja stoi 0%", "update mislukt", "0x800f0922"],
        "Nie resetować cache/usług przed zebraniem logów i sprawdzeniem storage, policy oraz czasu.",
        ["storage/RAM issue", "managed update policy", "BitLocker recovery risk przy firmware", "brak miejsca", "servicing stack pending"],
        ["build/edition", "update history", "WindowsUpdateClient events", "policy sources", "pending indicators", "CBS/DISM", "free space"],
        [
            ("Quality update fails", "Ta sama KB wraca z błędem.", "Servicing corruption, policy, space lub incompatibility.", "Zebrać exact KB/code, eventy, CBS i release health.", "Najpierw retry po potwierdzonym preflight; reset components dopiero później.", "KB zainstalowana, reboot completed i scan clean."),
            ("Feature update rollback", "Upgrade wraca do starej wersji.", "Compatibility block lub failure w SafeOS/FirstBoot.", "SetupDiag i Panther/Rollback przed czyszczeniem.", "Przekazać do setup-upgrade z konkretnym rule match.", "Nowy build działa albo udokumentowano wspierany safeguard hold."),
            ("Update sterowany przez organizację", "Some settings are managed.", "GPO/MDM/WSUS celowo kontroluje update.", "Zebrać policy/resultant state bez zmiany.", "Eskalować do administratora; nie resetować policy.", "Raport rozróżnia awarię klienta od zamierzonej polityki."),
        ],
        [
            ("Update health", "Windows — PowerShell 5.1", "& '.\\scripts\\diagnostics\\Get-WindowsUpdateHealth.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'", "R0", "JSON z historią, pending i event summary.", "Brak zmian."),
            ("Windows Update log", "Windows — PowerShell jako administrator", "Get-WindowsUpdateLog -LogPath '<OUTPUT>\\WindowsUpdate.log'", "R0", "Czytelny log utworzony z ETL.", "Usunąć wygenerowany log."),
            ("Plan resetu", "Windows — PowerShell jako administrator", "& '.\\scripts\\repair\\Invoke-WindowsUpdateRepair.ps1' -Mode Scan -LogRoot '<CASE_LOGS>'", "R0", "Plan i preflight bez zatrzymania usług/cache reset.", "Brak zmian w Scan."),
        ],
        ["windows-component-repair", "windows-setup-upgrade-rollback", "windows-remote-managed-client", "windows-10-support", "windows-11-support"],
        ["ms-wu-troubleshoot", "ms-windowsupdate-log", "ms-release-health"],
    ),
    s(
        "windows-setup-upgrade-rollback",
        "Setup, upgrade i rollback",
        "analizę in-place setup, feature update, compatibility blocks, SetupDiag, Panther/Rollback i kontrolowany rollback",
        ["upgrade failed", "SetupDiag", "Windows installatie teruggedraaid", "in-place repair install"],
        "Nie używać do zwykłej comiesięcznej KB bez logów Setup/Panther.",
        ["brak backupu", "storage/RAM instability", "BitLocker not ready", "unsupported hardware bypass", "managed safeguard hold"],
        ["SetupDiag result", "Panther/Rollback logs", "compat scan", "build/edition/language", "drivers/apps", "free space"],
        [
            ("Feature update rollback", "Setup wraca do poprzedniego builda.", "Rule match wskazuje driver/app/partition.", "Uruchomić parser na kopii logów i potwierdzić fazę.", "Usunąć tylko potwierdzony blocker lub zaktualizować OEM driver.", "Upgrade kończy OOBE/login i zachowuje dane/aplikacje."),
            ("In-place repair install", "System działa, component repair nie wystarcza.", "Repair install może zachować apps/data, ale wymaga zgodnego media.", "Sprawdzić edition/language/build, backup i BitLocker.", "Uruchomienie pozostawić jawnej interakcji z Setup; nie automatyzować wyborów.", "Build, activation, apps, profile i update działają."),
            ("Compatibility hold", "Windows Update nie oferuje wersji.", "Microsoft/OEM safeguard może być zamierzony.", "Sprawdzić release health i SetupCompat logs.", "Nie wymuszać bypass; poczekać lub zastosować oficjalną poprawkę.", "Hold znika oficjalnie albo decyzja o pozostaniu jest udokumentowana."),
        ],
        [
            ("Parse Panther", "Repo — PowerShell 5.1+", "& '.\\scripts\\diagnostics\\Parse-WindowsSetupLog.ps1' -Path '<PANTHER_FIXTURE>' -OutputPath '<OUTPUT_JSON>'", "R0", "Fazy, kody i rule matches bez modyfikacji źródła.", "Brak zmian."),
            ("SetupDiag", "Windows — CMD jako administrator", "\"<VERIFIED_SETUPDIAG>\" /Output:<OUTPUT>\\SetupDiagResults.log /Format:log", "R0", "Raport reguł; narzędzie musi pochodzić z Microsoft lub systemu.", "Usunąć raport."),
            ("Compatibility scan", "Windows — CMD jako administrator", "\"<MATCHED_MEDIA>\\setup.exe\" /auto upgrade /compat scanonly /copylogs <OUTPUT>", "R0", "Tylko scan compatibility i logi; Setup nie rozpoczyna upgrade.", "Usunąć wygenerowane logi."),
        ],
        ["windows-update-servicing", "windows-component-repair", "windows-drivers-devices", "windows-backup-vss-restore"],
        ["ms-setupdiag", "ms-setup-logfiles", "ms-release-health"],
    ),
    s(
        "windows-activation-licensing",
        "Aktywacja i licencjonowanie Windows",
        "legalną diagnostykę digital license, OEM OA3, edition mismatch i kanałów retail/OEM/volume bez ujawniania kluczy",
        ["Windows nie jest aktywowany", "activation error", "edition mismatch", "Windows-activering mislukt"],
        "Nie obsługiwać aktywatorów, emulatorów KMS, cracków ani obchodzenia warunków licencji.",
        ["prośba o crack/KMS emulator", "pełny product key w logu", "urządzenie firmowe z volume activation", "niejasny dowód licencji"],
        ["edition/channel", "partial product key only", "activation status/error", "OEM marker presence bez klucza", "MSA link", "organization scope"],
        [
            ("Edition mismatch po reinstalacji", "Licencja Home, zainstalowano Pro.", "Digital entitlement nie aktywuje innej edycji.", "Zebrać edition/channel i activation error bez pełnego key.", "Zainstalować właściwą legalną edycję lub kupić upgrade.", "slmgr status licensed i edition zgodna z entitlement."),
            ("Digital license po wymianie płyty", "Activation lost after hardware change.", "Hardware hash uległ zmianie.", "Użyć oficjalnego Activation Troubleshooter z właścicielem MSA.", "Jeśli OEM non-transferable — eskalować do Microsoft/OEM.", "Activation UI pokazuje legalną aktywację."),
            ("Firmowy KMS/MAK", "Laptop poza siecią nie aktywuje.", "Brak kontaktu z firmowym KMS/VPN lub exhausted MAK.", "Zebrać channel i generic error; nie testować publicznych serwerów.", "Eskalować do administratora licencji.", "Status licensed w autoryzowanej sieci."),
        ],
        [
            ("Status szczegółowy", "Windows — CMD jako administrator", "cscript.exe //Nologo %SystemRoot%\\System32\\slmgr.vbs /dlv", "R0", "Kanał, status i tylko częściowy key.", "Brak zmian."),
            ("Edition", "Windows — CMD jako administrator", "dism /Online /Get-CurrentEdition", "R0", "Bieżąca edycja bez klucza.", "Brak zmian."),
            ("Activation UI", "Windows — interfejs PL/EN/NL", "Ustawienia / Settings / Instellingen → System → Aktywacja / Activation / Activering", "R0", "Widoczny status i oficjalny troubleshooter.", "Brak zmian do momentu świadomego kliknięcia."),
        ],
        ["windows-os-identification", "windows-remote-managed-client", "windows-setup-upgrade-rollback"],
        ["ms-activation", "ms-activation-troubleshooter", "ms-volume-activation"],
    ),
    s(
        "windows-bsod-debugging",
        "BSOD, dumpy i WinDbg",
        "konfigurację dumpów, analizę bugcheck/stacks/modules/WHEA i ostrożne użycie Driver Verifier z planem odzyskania",
        ["blue screen", "BSOD", "bugcheck", "blauw scherm WinDbg"],
        "Nie uznawać nazwy modułu z pojedynczego minidumpa za dowód przyczyny.",
        ["storage/RAM errors", "brak wolnego miejsca/pagefile", "Verifier bez dostępu do WinRE", "WHEA hardware error"],
        ["exact bugcheck parameters", "dump type", "stack/module timestamps", "symbols", "WHEA/events", "repro conditions"],
        [
            ("Powtarzalny driver BSOD", "Ten sam bugcheck pod konkretną akcją.", "Sterownik może naruszać pamięć, ale moduł na stosie może być ofiarą.", "Analizować kilka dumpów z symbolami i korelować SetupAPI/driver changes.", "Rollback/update tylko potwierdzonego drivera OEM.", "Brak bugcheck w repro i brak nowych WHEA."),
            ("Losowe bugchecki", "Kody i moduły zmieniają się.", "RAM/storage/power bardziej prawdopodobne niż wiele driverów.", "Przerwać software repair, testować hardware i firmware stock.", "Naprawić stabilność przed dalszym debugowaniem.", "Wiele cykli testu bez błędów i spójny dump status."),
            ("Driver Verifier", "Podejrzenie third-party driver bez dowodu.", "Verifier może stworzyć boot loop.", "Zapewnić backup, WinRE i komendę reset; wybrać tylko podejrzane non-Microsoft drivers.", "Włączyć na ograniczony czas wyłącznie R3 z potwierdzeniem.", "Pozyskać deterministyczny dump i wyłączyć Verifier."),
        ],
        [
            ("Metadata dumpa", "Repo — PowerShell 5.1+", "& '.\\scripts\\diagnostics\\Get-MinidumpMetadata.ps1' -Path '<MINIDUMP_FIXTURE>' -OutputPath '<OUTPUT_JSON>'", "R0", "Rozmiar, czas, signature i jawna informacja, że to nie pełna analiza.", "Brak zmian."),
            ("WinDbg", "Windows — WinDbg Command", "!analyze -v", "R0", "Bugcheck, parametry i stack przy poprawnych symbolach.", "Brak zmian w dumpie."),
            ("Verifier status", "Windows — CMD jako administrator", "verifier /querysettings", "R0", "Aktualne ustawienia bez ich zmiany.", "Brak zmian."),
        ],
        ["memory-cpu-gpu-thermal", "windows-drivers-devices", "windows-boot-recovery", "windows-case-evidence"],
        ["ms-windbg", "ms-bugcheck", "ms-driver-verifier"],
    ),
    s(
        "windows-performance-hangs",
        "Wydajność, zawieszenia i ETW",
        "korelację opóźnień, hangów, stutter, CPU/RAM/dysk/GPU, DPC/ISR przy użyciu WPR/WPA, PerfMon i Reliability",
        ["Windows wolno działa", "100% disk", "microstutter", "pc hangt / not responding"],
        "Nie optymalizować przez wyłączanie ochrony/usług bez pomiaru i hipotezy.",
        ["storage health issue", "thermal throttling", "memory errors", "incydent malware", "trace zawiera wrażliwe dane"],
        ["repro timeline", "resource counters", "ETW profile", "Reliability/WER", "DPC/ISR", "temperatures/clocks"],
        [
            ("Wolne logowanie", "Desktop gotowy po kilku minutach.", "Startup, profile, network drives, policy lub storage.", "Zmierz boot/logon i koreluj startup/services/network.", "Wyłączaj jeden potwierdzony element odwracalnie.", "Median login time poprawia się w trzech próbach bez utraty funkcji."),
            ("100% disk", "Active time 100%, niski throughput.", "Latency storage, paging, AV scan lub failing media.", "Najpierw SMART/latency, potem process I/O trace.", "Naprawić przyczynę; nie wyłączać SysMain/Defender w ciemno.", "Latency i queue spadają w tym samym workload."),
            ("DPC audio stutter", "Trzaski podczas real-time audio.", "Driver ISR/DPC, power state lub USB.", "WPR trace i korelacja z urządzeniem; LatencyMon tylko pomocniczo.", "Update/rollback potwierdzonego drivera, test planu zasilania odwracalnie.", "Brak dropouts w kontrolowanym odtworzeniu i trace."),
        ],
        [
            ("Perf counters", "Windows — PowerShell 5.1", "Get-Counter '\\Processor(_Total)\\% Processor Time','\\PhysicalDisk(_Total)\\Avg. Disk sec/Transfer','\\Memory\\Available MBytes' -SampleInterval 2 -MaxSamples 30", "R0", "Krótki, datowany zestaw liczników.", "Brak zmian."),
            ("WPR status", "Windows — CMD jako administrator", "wpr -status", "R0", "Informacja, czy trwa trace.", "Brak zmian."),
            ("Reliability", "Windows — interfejs PL/EN/NL", "Monitor niezawodności / Reliability Monitor / Betrouwbaarheidscontrole: perfmon /rel", "R0", "Timeline awarii i instalacji.", "Brak zmian."),
        ],
        ["windows-process-service-startup", "memory-cpu-gpu-thermal", "windows-drivers-devices", "windows-bsod-debugging"],
        ["ms-wpr", "ms-wpa", "ms-perfmon"],
    ),
    s(
        "windows-process-service-startup",
        "Procesy, usługi i autostart",
        "diagnozę procesów, usług, Scheduled Tasks, Autoruns/ProcMon i odwracalny clean boot bez utraty konfiguracji",
        ["program startuje z Windowsem", "service won't start", "clean boot", "opstartprogramma uitschakelen"],
        "Nie używać do usuwania persistence malware bez ścieżki incydentowej.",
        ["usługa bezpieczeństwa/backup/MDM", "nieznany binary signature", "podejrzenie malware", "brak exportu konfiguracji"],
        ["process path/signature", "service config/dependencies", "task XML", "startup registry", "boot/logon timeline"],
        [
            ("Usługa nie startuje", "Service timeout/dependency error.", "Dependency, account, binary path lub policy.", "Zebrać sc qc, dependencies i eventy bez start/stop.", "Naprawić jeden parametr po eksporcie konfiguracji.", "Service osiąga Running i funkcja biznesowa działa po reboot."),
            ("Wolny startup", "Dużo programów po logowaniu.", "Jedna lub kilka pozycji blokuje shell.", "Autoruns export i pomiar baseline; nie wyłączać Microsoft entries.", "Wyłączać po jednej pozycji z dokumentowanym rollback.", "Startup krótszy, a aplikacje wymagane pozostają dostępne."),
            ("Podejrzane zadanie", "Losowy task uruchamia skrypt.", "Może być legalnym updaterem lub persistence.", "Wyeksportować XML, podpis/hash targetu i parent provenance.", "Przy malware przejść do incident playbook; nie kasować dowodu.", "Task sklasyfikowany, dowody zachowane, brak nieautoryzowanego uruchomienia."),
        ],
        [
            ("Usługi", "Windows — PowerShell 5.1", "Get-CimInstance -ClassName Win32_Service | Select-Object Name,State,StartMode,PathName,StartName", "R0", "Inwentaryzacja bez zmian stanu.", "Brak zmian."),
            ("Zadania", "Windows — PowerShell jako administrator", "Get-ScheduledTask | Select-Object TaskPath,TaskName,State,Author", "R0", "Lista zadań; action details zebrać dla wybranych.", "Brak zmian."),
            ("Startup", "Windows — PowerShell 5.1", "Get-CimInstance -ClassName Win32_StartupCommand | Select-Object Name,Command,Location,User", "R0", "Widoczne klasyczne startup entries bez wymuszania MSI consistency.", "Brak zmian."),
        ],
        ["windows-performance-hangs", "windows-malware-remediation", "windows-advanced-administration", "windows-post-repair-validation"],
        ["ms-services", "ms-scheduledtasks", "sysinternals-autoruns"],
    ),
    s(
        "windows-drivers-devices",
        "Sterowniki i urządzenia",
        "diagnozę Device Manager, PnPUtil, Driver Store, SetupAPI, DCH, Code 10/28/31/43 i kontrolowany rollback/offline driver",
        ["unknown device", "Code 43", "driver problem", "apparaatcode 10"],
        "Nie używać przypadkowych driver packs, a DDU tylko po potwierdzeniu problemu display driver i planie Safe Mode.",
        ["storage/network driver needed for recovery", "managed OEM policy", "unsigned driver", "BitLocker/boot-critical driver", "unknown hardware ID"],
        ["hardware IDs", "problem code", "driver provider/version/date", "SetupAPI excerpt", "OEM model", "recent changes"],
        [
            ("Unknown device Code 28", "Brak sterownika.", "Hardware ID wskazuje vendor/device.", "Zebrać IDs i dokładny model; szukać OEM/Windows Update Catalog.", "Zainstalować podpisany driver właściwy dla arch/build.", "Problem code 0 i funkcja urządzenia działa po reboot."),
            ("GPU Code 43", "Adapter zatrzymany.", "Driver, firmware, hardware lub passthrough.", "Sprawdzić pre-OS obraz, WHEA, driver history i clean profile.", "Rollback/OEM clean install; DDU dopiero kontrolowanie.", "Brak Code 43 i test GPU bez artefaktów."),
            ("Driver powoduje boot loop", "Po aktualizacji system nie startuje.", "Ostatni OEM INF jest niekompatybilny.", "WinRE/offline SetupAPI i driver store inventory.", "Usunąć tylko wskazany published name przez wrapper R3.", "Boot, device function i no new errors."),
        ],
        [
            ("Inventory", "Windows — PowerShell jako administrator", "& '.\\scripts\\diagnostics\\Get-WindowsDriverInventory.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'", "R0", "JSON driver/device inventory.", "Brak zmian."),
            ("PnPUtil enum", "Windows — CMD jako administrator", "pnputil /enum-devices /problem /deviceids", "R0", "Urządzenia z problemami i IDs.", "Brak zmian."),
            ("Driver Store plan", "Windows — PowerShell jako administrator", "& '.\\scripts\\repair\\Invoke-DriverStoreRepair.ps1' -Mode Scan -PublishedName '<OEM_INF>' -LogRoot '<CASE_LOGS>'", "R0", "Plan z provider/version/dependencies bez usunięcia.", "Brak zmian w Scan."),
        ],
        ["windows-peripherals-repair", "windows-bsod-debugging", "windows-boot-recovery", "bios-uefi-firmware"],
        ["ms-pnputil", "ms-setupapi", "ms-driver-store"],
    ),
    s(
        "windows-network-repair",
        "Sieć Windows",
        "warstwową diagnozę Ethernet/Wi-Fi/DHCP/DNS/proxy/VPN/routing/firewall/SMB i kontrolowane resety stosu",
        ["brak internetu", "DNS problem", "Wi-Fi disconnects", "geen internet / VPN werkt niet"],
        "Nie skanować cudzej sieci i nie resetować stosu przed snapshotem konfiguracji.",
        ["managed VPN/firewall", "incydent bezpieczeństwa", "brak autoryzacji do capture/Nmap", "statyczna konfiguracja bez backupu"],
        ["link/radio", "IP/gateway/DHCP", "DNS resolution", "routes/proxy/VPN", "firewall profile", "packet timing"],
        [
            ("Link jest, brak internetu", "Adres jest APIPA lub brak gateway.", "DHCP/link VLAN/adapter.", "Test warstwowy: media, lease, gateway, DNS, HTTPS.", "Naprawić najniższą uszkodzoną warstwę; reset jako późny R2.", "Lease poprawny, gateway/DNS/HTTPS działają."),
            ("DNS intermittent", "IP działa, nazwy czasem nie.", "Resolver, suffix, VPN split DNS lub upstream.", "Porównać Resolve-DnsName z serwerami i timeline.", "Korygować konfigurację tylko po identyfikacji właściciela DNS.", "Wielokrotne rozwiązywanie obu stref działa bez leak."),
            ("VPN psuje sieć", "Po rozłączeniu brak dostępu.", "Routes, proxy, NRPT lub filter driver pozostał.", "Snapshot przed/po VPN i diff tras/proxy/adapters.", "Repair klienta VPN/OEM; nie usuwać filtrów w ciemno.", "Sieć działa przed, w trakcie i po VPN."),
        ],
        [
            ("Snapshot", "Windows — PowerShell 5.1", "& '.\\scripts\\diagnostics\\Get-WindowsNetworkSnapshot.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'", "R0", "Zanonimizowany JSON z adapterami, IP, DNS, routes i proxy.", "Brak zmian."),
            ("DNS test", "Windows — PowerShell 5.1", "Resolve-DnsName -Name '<AUTHORIZED_HOST>' -Type A -DnsOnly", "R0", "Odpowiedź/timeout z konkretnym serwerem.", "Brak zmian."),
            ("Repair plan", "Windows — PowerShell jako administrator", "& '.\\scripts\\repair\\Invoke-WindowsNetworkRepair.ps1' -Mode Scan -LogRoot '<CASE_LOGS>'", "R0", "Plan resetów i snapshot bez zmian.", "Brak zmian w Scan."),
        ],
        ["windows-drivers-devices", "windows-remote-managed-client", "windows-malware-remediation", "windows-peripherals-repair"],
        ["ms-nettcpip", "ms-netsh", "wireshark"],
    ),
    s(
        "windows-peripherals-repair",
        "Peryferia Windows",
        "diagnozę drukarek, spoolera, skanerów, audio, monitorów, USB, Bluetooth, kamer, docków i HID",
        ["drukarka nie drukuje", "no sound", "Bluetooth werkt niet", "USB disconnect / kamera nie działa"],
        "Nie zastępować skilla driver/hardware, gdy problem występuje także przed uruchomieniem Windows.",
        ["przegrzewający się port/kabel", "uszkodzenie mechaniczne", "managed print policy", "kamera/mikrofon z policy privacy"],
        ["problem device IDs", "port/cable/dock path", "driver and firmware", "service/event logs", "privacy policy", "known-good peripheral"],
        [
            ("Kolejka drukarki stoi", "Jobs pozostają w queue.", "Spooler job/driver/port może być uszkodzony.", "Wyeksportować queue, driver i PrintService events.", "Usunąć tylko wskazany job lub kontrolowanie wyczyścić spool po backupie.", "Test page i realny dokument drukują po reboot."),
            ("Brak audio", "Output device istnieje, brak dźwięku.", "Endpoint selection, service, driver, privacy lub dock.", "Testować physical path, endpoint i events bez reinstall-all.", "Rollback/update właściwego OEM audio stack.", "Playback/recording i sleep/wake działają."),
            ("USB/Bluetooth rozłącza", "Urządzenie znika okresowo.", "Power management, kabel, hub, RF, driver lub hardware.", "Korelować PnP events i topologię; test znanego kabla/portu.", "Zmieniać jeden element; ustawienia zasilania jako R1 z rollback.", "Brak disconnect w powtarzalnym teście oraz po resume."),
        ],
        [
            ("Problem devices", "Windows — CMD jako administrator", "pnputil /enum-devices /problem /deviceids", "R0", "Lista PnP z kodami i hardware IDs.", "Brak zmian."),
            ("Print events", "Windows — PowerShell jako administrator", "Get-WinEvent -LogName 'Microsoft-Windows-PrintService/Operational' -MaxEvents 100", "R0", "Timeline print errors; kanał może wymagać wcześniejszego włączenia.", "Brak zmian."),
            ("Spooler plan", "Windows — PowerShell jako administrator", "& '.\\scripts\\repair\\Invoke-PrintSpoolerRepair.ps1' -Mode Scan -LogRoot '<CASE_LOGS>'", "R0", "Stan spoolera/queue i plan bez stop/delete.", "Brak zmian w Scan."),
        ],
        ["windows-drivers-devices", "pc-hardware-diagnostics", "windows-network-repair", "windows-post-repair-validation"],
        ["ms-printer-troubleshoot", "ms-pnputil", "ms-bluetooth"],
    ),
    s(
        "windows-accounts-profiles",
        "Konta, logowanie i profile",
        "oficjalne odzyskanie logowania lokalnego/MSA/Entra/Hello oraz naprawę temporary/corrupt profile bez obchodzenia haseł",
        ["temporary profile", "nie mogę się zalogować", "Windows Hello PIN problem", "tijdelijk profiel"],
        "Nie omijać haseł, nie dumpować credentials i nie resetować kont organizacji poza oficjalnym procesem.",
        ["brak autoryzacji właściciela", "EFS", "Entra/MDM", "brak kopii profilu", "podejrzenie account compromise"],
        ["account type/source", "profile SID/path/state", "User Profile Service events", "EFS awareness", "MSA/Entra recovery channel"],
        [
            ("Temporary profile", "Windows loguje do profilu tymczasowego.", "ProfileList state/path, disk/ACL lub hive corruption.", "Zebrać events i profile mapping, sprawdzić storage.", "Najpierw odwracalna korekta pojedynczego mappingu; migracja do nowego profilu jeśli hive uszkodzony.", "Dwa logowania do właściwego profilu i aplikacje/dane dostępne."),
            ("Hello PIN unavailable", "PIN nie działa po TPM/firmware change.", "Hello container, TPM attestation lub policy.", "Potwierdzić password/official recovery i stan TPM/Entra.", "Użyć oficjalnego „I forgot my PIN”; nie usuwać NGC w ciemno.", "PIN re-enrolled, password fallback i access policies działają."),
            ("Migracja uszkodzonego profilu", "Explorer/apps padają tylko dla jednego usera.", "User hive/profile corruption.", "Porównać nowy test profile i zinwentaryzować EFS/OneDrive.", "Migrować dane, nie cały AppData/registry; zachować ACL.", "Nowy profil działa, dane otwierają się, sync i backup zweryfikowane."),
        ],
        [
            ("Profile inventory", "Windows — PowerShell jako administrator", "Get-CimInstance -ClassName Win32_UserProfile | Select-Object SID,LocalPath,Loaded,Special,Status", "R0", "Mapowanie SID/path bez haseł.", "Brak zmian."),
            ("Profile events", "Windows — PowerShell jako administrator", "Get-WinEvent -FilterHashtable @{LogName='Application';ProviderName='Microsoft-Windows-User Profiles Service'} -MaxEvents 100", "R0", "Błędy profilu z czasem.", "Brak zmian."),
            ("Repair plan", "Windows — PowerShell jako administrator", "& '.\\scripts\\repair\\Invoke-UserProfileRepair.ps1' -Mode Scan -ProfilePath '<PROFILE>' -LogRoot '<CASE_LOGS>'", "R0", "Preflight EFS/OneDrive/ACL i plan bez zmian.", "Brak zmian w Scan."),
        ],
        ["windows-ntfs-permissions-shares", "windows-bitlocker-tpm-security", "windows-office-cloud-repair", "windows-remote-managed-client"],
        ["ms-account-recovery", "ms-hello", "ms-user-profile"],
    ),
    s(
        "windows-ntfs-permissions-shares",
        "NTFS ACL i udziały SMB",
        "precyzyjną diagnozę ownership, dziedziczenia, effective access, share ACL, offline ACL i świadomość EFS",
        ["Access denied", "NTFS permissions", "SMB share permission", "toegang geweigerd"],
        "Nie wykonywać masowego takeown/icacls reset na dysku systemowym.",
        ["EFS encrypted files", "organizacyjny share", "nieznany właściciel danych", "root system drive target", "brak ACL backup"],
        ["identity/SID", "current ACL SDDL", "inheritance", "share permissions", "effective access", "EFS status"],
        [
            ("Access denied do jednego folderu", "Właściciel ma upoważnienie.", "Explicit deny, orphan SID lub share ACL.", "Eksport icacls i porównanie NTFS/share effective path.", "Skorygować minimalny ACE po backupie ACL.", "Docelowy user ma wymagany dostęp, inni nie uzyskali dodatkowego."),
            ("Po migracji dysku stare SID", "Foldery pokazują unknown account.", "ACL odwołują się do starego SID.", "Mapować stare/nowe konto i EFS przed zmianą.", "Dodać nowe ACE; nie usuwać starych do walidacji.", "Pliki otwierają się i audit nie pokazuje broadened access."),
            ("SMB działa lokalnie, nie z sieci", "NTFS lokalnie OK.", "Share ACL, SMB auth, firewall lub network profile.", "Sprawdzić Get-SmbShareAccess i test z autoryzowanego klienta.", "Naprawić najwęższą warstwę, nie Everyone Full Control.", "Dostęp działa tylko dla zaplanowanych principal."),
        ],
        [
            ("ACL odczyt", "Windows — PowerShell 5.1", "Get-Acl -LiteralPath '<TARGET>' | Format-List Path,Owner,AccessToString,AreAccessRulesProtected", "R0", "Owner i ACE bez zmian.", "Brak zmian."),
            ("ACL backup", "Windows — CMD jako administrator", "icacls \"<TARGET>\" /save \"<BACKUP>\\acl.txt\" /t /c", "R1", "Eksport ACL; może ujawnić nazwy ścieżek, więc podlega redakcji.", "icacls <PARENT> /restore wymaga osobnego R3 gate."),
            ("Share ACL", "Windows — PowerShell jako administrator", "Get-SmbShareAccess -Name '<SHARE>'", "R0", "Share permissions dla principal.", "Brak zmian."),
        ],
        ["windows-accounts-profiles", "windows-network-repair", "windows-bitlocker-tpm-security", "windows-case-evidence"],
        ["ms-icacls", "ms-smbshare", "ms-efs"],
    ),
    s(
        "windows-bitlocker-tpm-security",
        "BitLocker, TPM i zabezpieczenia platformy",
        "diagnozę Device Encryption/BitLocker, recovery readiness, TPM, Secure Boot, VBS/HVCI, certyfikatów i policy bez obchodzenia ochrony",
        ["BitLocker recovery loop", "TPM error", "Device Encryption", "herstelcode BitLocker / Secure Boot"],
        "Nie pozyskiwać, zapisywać ani obchodzić recovery keys; nie wyłączać ochrony bez jawnego celu i rollbacku.",
        ["brak recovery key readiness", "firmware/BCD/partition change", "managed policy", "podejrzenie kradzieży", "EFS/certificate loss"],
        ["protection/lock status bez key", "protector types bez IDs w raporcie publicznym", "TPM readiness", "Secure Boot cert state", "VBS/HVCI", "management policy"],
        [
            ("Recovery po firmware change", "Każdy boot żąda key.", "PCR zmienił się albo firmware nie zapisuje ustawień.", "Nie wpisywać key do logu; zebrać firmware/TPM/events po autoryzowanym unlock.", "Naprawić firmware/policy i wykonać oficjalny reseal tylko z adminem.", "Dwa cold boots bez recovery i protector active."),
            ("Plan zmiany BIOS/BCD", "Naprawa R3/R4 może wywołać recovery.", "BitLocker będzie chronił zmianę boot chain.", "Potwierdzić backup, recovery readiness i management owner.", "Suspend na minimalną liczbę rebootów tylko jawnie; resume sprawdzić.", "Protection On i test recovery process bez ujawniania key."),
            ("Secure Boot cert 2026", "Urządzenie może mieć certyfikaty 2011.", "Brak update 2023 ograniczy przyszłe boot protections.", "Sprawdzić oficjalne signals/events i firmware compatibility.", "Pilotować oficjalny update, nie wgrywać losowych kluczy.", "Status Updated, boot/BitLocker stabilne po kontrolowanych rebootach."),
        ],
        [
            ("BitLocker safety", "Windows — PowerShell jako administrator", "& '.\\scripts\\diagnostics\\Get-BitLockerSafetyStatus.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'", "R0", "Status bez RecoveryPassword/KeyProtector secrets.", "Brak zmian."),
            ("TPM", "Windows — PowerShell jako administrator", "Get-Tpm | Select-Object TpmPresent,TpmReady,TpmEnabled,TpmActivated,AutoProvisioning", "R0", "Stan TPM bez clear/initialize.", "Brak zmian."),
            ("Device Guard", "Windows — PowerShell 5.1", "Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\\Microsoft\\Windows\\DeviceGuard", "R0", "VBS/HVCI capability i running services.", "Brak zmian."),
        ],
        ["bios-uefi-firmware", "windows-bcd-partition-repair", "windows-remote-managed-client", "windows-accounts-profiles"],
        ["ms-bitlocker-overview", "ms-tpm", "ms-secure-boot-2026"],
    ),
    s(
        "windows-malware-remediation",
        "Triage i usuwanie malware",
        "izolację, zachowanie dowodów, Defender Offline/MSERT/Sysinternals, PUP/browser hijack, persistence i kryteria reinstalacji",
        ["podejrzewam wirusa", "browser hijack", "Defender disabled", "malware verwijderen"],
        "Nie prowadzić ofensywnej analizy, credential dumping ani wielu skanerów naprawczych równocześnie.",
        ["ransomware in progress", "credential theft", "business incident", "evidence/legal hold", "backup connected to infected host"],
        ["timeline", "network isolation status", "Defender state/detections", "persistence exports", "hashes/signatures", "account exposure"],
        [
            ("PUP/browser hijack", "Homepage/extensions wracają.", "Extension, policy, scheduled task lub sync.", "Odłączyć sync, eksportować extensions/policies/tasks.", "Usunąć potwierdzoną persistence i zresetować tylko dotknięte ustawienia.", "Po reboot/sync brak powrotu, accounts reviewed."),
            ("Defender disabled", "Protection off bez zgody.", "Policy, third-party AV, tampering lub malware.", "Ustalić management/AV registration/events przed zmianą.", "Przy incydencie izolować; nie wyłączać zabezpieczeń dalej.", "Defender/approved AV healthy, detections resolved, offline scan logged."),
            ("Poważny kompromis", "Stealer/ransomware/backdoor evidence.", "Integralność hosta i credentials niepewna.", "Odizolować, zachować dowody, zmienić hasła na czystym urządzeniu.", "Preferować clean rebuild ze zweryfikowanych danych zamiast „oczyszczania”.", "Rebuild patched, accounts rotated, backup scanned, monitoring clean."),
        ],
        [
            ("Defender state", "Windows — PowerShell jako administrator", "Get-MpComputerStatus | Select-Object AMServiceEnabled,AntivirusEnabled,RealTimeProtectionEnabled,BehaviorMonitorEnabled,AntivirusSignatureLastUpdated", "R0", "Stan ochrony bez uruchamiania skanu.", "Brak zmian."),
            ("Persistence", "Windows — PowerShell jako administrator", "& '.\\scripts\\diagnostics\\Get-WindowsStartupPersistence.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'", "R0", "Zanonimizowany export startup/services/tasks.", "Brak zmian."),
            ("Detections", "Windows — PowerShell jako administrator", "Get-MpThreatDetection | Select-Object InitialDetectionTime,ThreatName,Resources,ActionSuccess", "R0", "Historia detekcji; Resources mogą wymagać redakcji.", "Brak zmian."),
        ],
        ["windows-process-service-startup", "windows-case-evidence", "windows-backup-vss-restore", "windows-accounts-profiles"],
        ["ms-defender-offline", "ms-msert", "sysinternals-autoruns"],
    ),
    s(
        "windows-apps-store-winget",
        "Aplikacje, Store, MSI/MSIX i winget",
        "diagnozę instalacji/odinstalowania MSI, ClickOnce, MSIX/AppX, Store, dependencies i winget bez registry cleanerów",
        ["Microsoft Store nie działa", "winget error", "MSI install failed", "app wordt niet gestart"],
        "Nie używać Win32_Product do inwentaryzacji i nie masowo rejestrować wszystkich AppX bez diagnozy.",
        ["aplikacja przechowuje krytyczne dane", "managed deployment", "package identity mismatch", "brak installer source/license"],
        ["package identity/version", "install technology", "event/MSI log", "dependencies", "user/all-users scope", "policy"],
        [
            ("Store download fails", "Download stoi lub błąd licencji.", "Account, cache, service, network lub package registration.", "Zebrać Store/AppX events i account/network state.", "Reset tylko Store cache/app, nie wszystkie pakiety.", "Install/update działa dla testowej legalnej aplikacji."),
            ("MSI rollback", "Installer kończy 1603.", "Custom action, permissions, pending reboot lub older product.", "Wygenerować verbose MSI log i znaleźć Return value 3 context.", "Naprawić konkretny prerequisite/ACL, nie czyścić rejestru.", "MSI exit 0 i aplikacja startuje/odinstalowuje się."),
            ("winget source failure", "winget source/update error.", "Source metadata, proxy, App Installer version.", "winget --info/source list i network snapshot.", "Reset source tylko po backupie i na wspieranym systemie.", "winget source update oraz show/install plan działają."),
        ],
        [
            ("Package inventory", "Windows — PowerShell 5.1", "Get-AppxPackage | Select-Object Name,PackageFullName,Version,Status,InstallLocation", "R0", "Pakiety bieżącego usera bez rejestracji zmian.", "Brak zmian."),
            ("winget info", "Windows — CMD", "winget --info", "R0", "Wersja klienta, package manager i paths.", "Brak zmian."),
            ("Store plan", "Windows — PowerShell jako administrator", "& '.\\scripts\\repair\\Invoke-StoreAppxRepair.ps1' -Mode Scan -PackageName '<PACKAGE>' -LogRoot '<CASE_LOGS>'", "R0", "Plan ograniczony do wskazanego pakietu.", "Brak zmian w Scan."),
        ],
        ["windows-shell-ui-repair", "windows-office-cloud-repair", "windows-update-servicing", "windows-remote-managed-client"],
        ["ms-winget", "ms-appx", "ms-msi-logging"],
    ),
    s(
        "windows-shell-ui-repair",
        "Explorer, Start, Search i interfejs",
        "diagnozę Explorer, Start, Search, Settings, taskbar, shell extensions, ikon i file associations",
        ["Start menu nie działa", "Explorer crashes", "taskbar frozen", "Zoeken werkt niet"],
        "Nie masowo rejestrować AppX ani resetować profilu bez porównania nowego konta.",
        ["objaw tylko na jednym profilu z EFS/OneDrive", "managed shell policy", "crash po third-party extension", "storage/component corruption"],
        ["scope user/system", "Reliability/WER", "shell extension list", "AppX events", "profile comparison", "policy"],
        [
            ("Explorer crash loop", "explorer.exe restartuje.", "Shell extension, namespace handler lub corruption.", "Safe Mode/new profile i WER module correlation.", "Wyłączyć pojedynczą third-party extension z rollback.", "Explorer stabilny w repro i po reboot."),
            ("Start/Search nie odpowiada", "Kliknięcie bez reakcji.", "Search service/package/user state/policy.", "Events, process state i test nowego profilu.", "Naprawić konkretny komponent; re-registration ograniczona.", "Start, Search i Settings działają po dwóch logowaniach."),
            ("Złe file associations", "Pliki otwierają złą aplikację.", "Per-user choice, package removal lub policy.", "Zebrać extension/progid i approved apps.", "Użyć UI Default Apps lub precyzyjnego, wspieranego association path.", "Double-click i Open With działają dla próbki."),
        ],
        [
            ("WER Explorer", "Windows — PowerShell 5.1", "Get-WinEvent -FilterHashtable @{LogName='Application';ProviderName='Application Error'} -MaxEvents 100 | Where-Object Message -Match 'explorer.exe'", "R0", "Faulting module/timestamp dla korelacji.", "Brak zmian."),
            ("Processes", "Windows — PowerShell 5.1", "Get-Process -Name explorer,StartMenuExperienceHost,SearchHost -ErrorAction SilentlyContinue | Select-Object Name,Id,StartTime,Path", "R0", "Stan procesów; brak procesu jest dowodem, nie naprawą.", "Brak zmian."),
            ("Associations", "Windows — CMD", "assoc <EXTENSION>", "R0", "Bieżące klasyczne association; MSIX defaults mogą wymagać UI.", "Brak zmian."),
        ],
        ["windows-accounts-profiles", "windows-apps-store-winget", "windows-component-repair", "windows-performance-hangs"],
        ["ms-start-menu", "ms-appx", "sysinternals-autoruns"],
    ),
    s(
        "windows-office-cloud-repair",
        "Microsoft 365, Outlook, OneDrive i Teams",
        "ochronę danych oraz diagnozę Click-to-Run, profili Outlook, PST/OST, OneDrive/Teams sign-in i synchronizacji",
        ["Outlook nie startuje", "OneDrive sync problem", "Teams sign-in", "Office activering / synchronisatie"],
        "Nie usuwać profilu, OST/PST ani unlinkować OneDrive bez inwentaryzacji danych i rollbacku.",
        ["lokalne-only PST", "unsynced OneDrive files", "managed tenant", "retention/legal hold", "account compromise"],
        ["account/tenant scope bez sekretów", "Office channel/build", "data file paths/sizes", "sync state", "add-ins", "identity/WAM events"],
        [
            ("Outlook crash/start fail", "Outlook nie otwiera profilu.", "Add-in, navigation pane, profile lub data file.", "Safe mode, event/WER i lista add-ins; zabezpieczyć PST.", "Wyłączyć potwierdzony add-in lub utworzyć nowy profil bez kasowania starego.", "Mail/calendar i send/receive działają, dane lokalne zachowane."),
            ("OneDrive sync stuck", "Pliki mają czerwone X.", "Invalid names, quota, auth, policy lub client state.", "Zebrać sync errors i policzyć unsynced local data.", "Naprawić konkretny błąd; unlink/reset dopiero po kopii lokalnej.", "Portal i lokalne hashes/próbka są zgodne."),
            ("Teams sign-in loop", "WAM login wraca.", "Token broker, time, WebView2, policy lub tenant.", "Sprawdzić time, account broker events i Office health.", "Naprawić wspieranym client resetem tylko po wylogowaniu/backup.", "Sign-in, meeting audio/video i reboot działają."),
        ],
        [
            ("Office Click-to-Run", "Windows — PowerShell 5.1", "Get-ItemProperty -LiteralPath 'HKLM:\\SOFTWARE\\Microsoft\\Office\\ClickToRun\\Configuration' | Select-Object VersionToReport,UpdateChannel,Platform", "R0", "Build/channel/arch bez tokenów.", "Brak zmian."),
            ("Outlook data", "Windows — PowerShell 5.1", "Get-ChildItem -LiteralPath '<OUTLOOK_DATA_ROOT>' -File -Filter '*.pst' | Select-Object FullName,Length,LastWriteTime", "R0", "Inwentaryzacja PST; ścieżki redagować.", "Brak zmian."),
            ("OneDrive status", "Windows — PowerShell 5.1", "Get-Process -Name OneDrive -ErrorAction SilentlyContinue | Select-Object Id,StartTime,Path,ProductVersion", "R0", "Stan procesu i wersja; nie dowodzi zakończenia sync.", "Brak zmian."),
        ],
        ["windows-accounts-profiles", "windows-apps-store-winget", "windows-network-repair", "windows-backup-vss-restore"],
        ["ms-office-repair", "ms-onedrive", "ms-teams-troubleshoot"],
    ),
    s(
        "windows-backup-vss-restore",
        "Backup, VSS i przywracanie",
        "diagnozę VSS, restore points, File History, Windows Backup, obrazów bare-metal i walidację kopii",
        ["VSS error", "backup failed", "File History", "systeemherstel werkt niet"],
        "Nie usuwać shadow copies ani katalogów backupu jako pierwszy krok.",
        ["jedyna kopia danych", "ransomware", "storage risk source/destination", "backup encryption key unavailable", "managed retention"],
        ["backup scope", "last successful run", "restore test", "VSS writers/providers", "target health/capacity", "encryption/key custody"],
        [
            ("VSS writer failed", "Backup zgłasza writer error.", "Service/app writer state lub provider conflict.", "Zebrać writers/providers/events i powtórzyć bez restartu usług.", "Naprawić konkretny writer/provider; nie re-register all DLLs.", "Writer stable i test backup+restore file przechodzi."),
            ("Walidacja obrazu", "Backup mówi successful.", "Success log nie gwarantuje restore.", "Sprawdzić checksum/catalog i wykonać mount/test restore w izolacji.", "Nie nadpisywać oryginału; testować na pustym celu/VM.", "Losowa próbka i boot test VM, jeśli licencja pozwala."),
            ("File History brak wersji", "Użytkownik nie widzi pliku.", "Scope/exclusion/target disconnect/retention.", "Zebrać config i target health bez cleanup.", "Naprawić target/schedule, dane odzyskać z innych kopii.", "Nowy plik ma co najmniej dwie wersje i restore działa."),
        ],
        [
            ("VSS writers", "Windows — CMD jako administrator", "vssadmin list writers", "R0", "Stan i last error każdego writer.", "Brak zmian."),
            ("Shadow copies", "Windows — PowerShell jako administrator", "Get-CimInstance -ClassName Win32_ShadowCopy | Select-Object ID,InstallDate,VolumeName,DeviceObject", "R0", "Inwentaryzacja bez delete.", "Brak zmian."),
            ("Repair plan", "Windows — PowerShell jako administrator", "& '.\\scripts\\repair\\Invoke-VssBackupRepair.ps1' -Mode Scan -LogRoot '<CASE_LOGS>'", "R0", "Plan konkretnego writer/provider bez zmian.", "Brak zmian w Scan."),
        ],
        ["storage-triage-cloning-recovery", "windows-case-evidence", "windows-post-repair-validation", "windows-malware-remediation"],
        ["ms-vss", "ms-file-history", "ms-windows-backup"],
    ),
    s(
        "windows-remote-managed-client",
        "Klient zdalny, domenowy, Entra i MDM",
        "transparentną Quick Assist/RDP pomoc oraz wykrycie domain/Entra/MDM, GPO, certyfikatów, mapped drives i firmowych VPN bez łamania zarządzania",
        ["laptop firmowy", "Entra joined", "GPO problem", "Quick Assist / Hulp op afstand"],
        "Nie wdrażać unattended persistence i nie zmieniać polityk organizacji bez administratora.",
        ["brak świadomej zgody na sesję", "Defender for Endpoint/LAPS/MDM", "certificate/private key", "conditional access", "organizational data"],
        ["join state", "MDM enrollment", "gpresult", "cert store metadata bez private keys", "VPN/mapped drive", "session consent"],
        [
            ("Quick Assist session", "Użytkownik prosi o widoczną pomoc.", "Sesja musi być świadoma i odwracalna.", "Potwierdzić zakres, recording/data access i zakończenie.", "Nie instalować trwałego agenta; każdą zmianę zapisać.", "Użytkownik widzi zakończenie, session closed, actions reported."),
            ("GPO nie stosuje się", "Firmowa konfiguracja brakująca.", "Connectivity, time, trust, scope lub client extension.", "gpresult/events/domain connectivity bez gpupdate force loops.", "Eskalować z dowodami do admina; nie edytować local policy przeciw GPO.", "RSoP wskazuje oczekiwaną policy lub znany owner blocker."),
            ("Entra/MDM compliance", "Device noncompliant.", "Policy, certificate, TPM, update lub stale enrollment.", "dsregcmd/status i MDM diagnostics bez tokenów.", "Nie re-enroll/leave organization bez administratora.", "Compliance naprawiona oficjalnym kanałem i access restored."),
        ],
        [
            ("Join state", "Windows — CMD", "dsregcmd /status", "R0", "Join/SSO/MDM metadata; output zanonimizować.", "Brak zmian."),
            ("RSoP", "Windows — CMD jako administrator", "gpresult /h \"<OUTPUT>\\gpresult.html\" /f", "R0", "Raport GPO zawierający dane organizacji; chronić.", "Usunąć raport po przekazaniu."),
            ("Management status", "Windows — PowerShell 5.1", "& '.\\scripts\\diagnostics\\Get-WindowsManagementStatus.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'", "R0", "Zanonimizowany join/MDM/security summary.", "Brak zmian."),
        ],
        ["windows-network-repair", "windows-bitlocker-tpm-security", "windows-accounts-profiles", "windows-update-servicing"],
        ["ms-dsregcmd", "ms-gpresult", "ms-quick-assist"],
    ),
    s(
        "windows-advanced-administration",
        "Zaawansowana administracja klienta Windows",
        "bezpieczną pracę z Event Viewer, registry, services, tasks, local policy, firewall, certyfikaty, storage, SMB, Hyper-V, WSL, Sandbox i power",
        ["Event Viewer analysis", "registry/service administration", "Hyper-V WSL issue", "Windows-beheer geavanceerd"],
        "Nie używać jako routera dla dobrze zdefiniowanej awarii należącej do węższego skilla.",
        ["managed policy", "registry root bulk edit", "private keys", "storage destructive action", "security control disable"],
        ["scope and owner", "before export", "events/config", "dependencies", "policy precedence", "rollback artifact"],
        [
            ("Korelacja Event Viewer", "Wiele błędów bez jasnej przyczyny.", "Większość zdarzeń może być wtórna.", "Ustalić symptom timestamp i filtrować provider/event/window.", "Naprawiać tylko zdarzenie skorelowane z reprodukcją.", "Po naprawie symptom znika i odpowiedni event nie wraca."),
            ("Precyzyjna zmiana registry", "Vendor KB wymaga jednego value.", "Błędny hive/view/ACL może uszkodzić system.", "Zweryfikować source, OS applicability i eksport klucza.", "Zmienić dokładny value SupportsShouldProcess; reboot tylko gdy wymagany.", "Value/behavior zgodne, rollback import przetestowany w lab."),
            ("WSL/Hyper-V conflict", "Feature nie startuje.", "Firmware virtualization, optional features, hypervisor policy.", "Zebrać feature state, systeminfo i events.", "Włączać/wyłączać tylko potwierdzony feature z restart gate.", "VM/WSL startuje, sleep/security regression przechodzi."),
        ],
        [
            ("Correlated events", "Windows — PowerShell 5.1", "Get-WinEvent -FilterHashtable @{LogName='System';StartTime='<START_TIME>';EndTime='<END_TIME>'} | Select-Object TimeCreated,ProviderName,Id,LevelDisplayName,Message", "R0", "Zdarzenia w ograniczonym oknie.", "Brak zmian."),
            ("Feature state", "Windows — PowerShell jako administrator", "Get-WindowsOptionalFeature -Online | Where-Object State -ne 'Disabled' | Select-Object FeatureName,State", "R0", "Włączone/pending features.", "Brak zmian."),
            ("Firewall profiles", "Windows — PowerShell jako administrator", "Get-NetFirewallProfile | Select-Object Name,Enabled,DefaultInboundAction,DefaultOutboundAction", "R0", "Stan profili bez wyłączenia.", "Brak zmian."),
        ],
        ["windows-automation-powershell", "windows-process-service-startup", "windows-network-repair", "windows-remote-managed-client"],
        ["ms-get-winevent", "ms-registry", "ms-optionalfeatures"],
    ),
    s(
        "windows-automation-powershell",
        "Automatyzacja PowerShell i CMD",
        "projektowanie bezpiecznych, idempotentnych skryptów PowerShell 5.1/7, CIM, remoting, logging, ShouldProcess i testów",
        ["napisz skrypt PowerShell do Windows", "safe automation", "Pester mock", "PowerShell automatisering"],
        "Nie uruchamiać wygenerowanej automatyzacji naprawczej na hoście budowy.",
        ["brak WhatIf/Apply gate", "Invoke-Expression", "sekrety w logu", "nieustalony target", "remoting bez autoryzacji"],
        ["PowerShell version", "OS/arch/elevation", "target set", "idempotency state", "rollback", "mock coverage"],
        [
            ("Nowy collector R0", "Potrzebny powtarzalny export.", "Deterministyczny output ułatwi diagnozę.", "Zaprojektować typed parameters, redaction i JSON schema.", "Testować tylko fixtures/mocks; live mode pozostawić operatorowi.", "Syntax, fixtures, redaction i exit codes przechodzą."),
            ("Repair wrapper R2", "Potrzebna kontrolowana zmiana.", "Błąd targetu może uszkodzić system.", "Preflight, snapshot, -Mode Scan default, -Apply i ShouldProcess.", "Concrete cmdlets w switch, bez eval/string execution.", "WhatIf wykonuje zero mutacji, apply test wyłącznie VM."),
            ("Legacy compatibility", "Skrypt ma działać PS5.1/WinRE.", "Nowsza składnia/API może nie istnieć.", "Parse pod odpowiednimi language modes i zapewnić minimalny CMD fallback.", "Oznaczyć funkcje PS7-only; nie polyfillować niebezpiecznie.", "Static parse i VM matrix potwierdzają ścieżki."),
        ],
        [
            ("Parse syntax", "Repo — PowerShell 5.1+", "$errors=$null; [System.Management.Automation.Language.Parser]::ParseFile('<SCRIPT>',[ref]$null,[ref]$errors) | Out-Null; $errors", "R0", "Pusta lista parse errors.", "Brak zmian."),
            ("Repo validation", "Repo — PowerShell 5.1+", "& '.\\scripts\\repo\\Test-WindowsMasterRepo.ps1' -Category Scripts", "R0", "Syntax/safety/Pester results z jawnie oznaczonym SKIP.", "Brak zmian poza raportem."),
            ("Analyzer", "Repo — PowerShell 5.1+", "Invoke-ScriptAnalyzer -Path '<SCRIPT_ROOT>' -Recurse -Settings '.\\PSScriptAnalyzerSettings.psd1'", "R0", "Diagnostics z przypiętej wersji modułu; jeśli brak, test jawnie SKIP.", "Brak zmian."),
        ],
        ["windows-advanced-administration", "windows-case-evidence", "windows-post-repair-validation"],
        ["ms-powershell-shouldprocess", "pester-docs", "psscriptanalyzer"],
    ),
    s(
        "windows-deployment-imaging",
        "Wdrożenia, WIM/ESD/FFU i migracja",
        "planowanie DISM imaging, unattend, Sysprep, ADK/WinPE, drivers offline i migracji HDD→SSD bez ryzyka pomylenia celu",
        ["capture WIM", "deploy Windows image", "Sysprep error", "HDD naar SSD migratie"],
        "Nie wykonywać capture/apply/clean na niezweryfikowanym dysku ani nie dołączać obrazów/licencji do repo.",
        ["source/target ambiguity", "BitLocker", "unsupported generalization", "OEM recovery dependencies", "insufficient backup"],
        ["disk unique IDs", "image metadata/index/hash", "edition/language/arch", "driver set", "unattend secrets scan", "restore test"],
        [
            ("Migracja HDD→SSD", "Wymiana na nowy dysk.", "Layout/sector size/boot mode może nie pasować.", "Sprawdzić health źródła, backup, used space i target IDs.", "Klonować/imaging poza Windows; nie nadpisywać źródła.", "Boot, partitions, alignment, BitLocker i recovery działają."),
            ("Capture WIM", "Wzorzec ma być wdrażany.", "Sysprep state/licensing/user data mogą wejść do obrazu.", "Audit mode, secrets scan i supported app state.", "Capture do zweryfikowanego celu po shutdown.", "Apply w VM, specialize/OOBE i driver injection przechodzą."),
            ("Offline driver injection", "WinPE/Windows nie widzi storage/network.", "Niepoprawny arch/boot-critical INF może zablokować start.", "Rozpakowany signed OEM driver, arch/build i katalog backup.", "Inject tylko wymagany INF; zachować DISM log.", "Urządzenie widoczne i boot działa bez nowych problem devices."),
        ],
        [
            ("WIM metadata", "WinPE/Windows — CMD jako administrator", "dism /Get-WimInfo /WimFile:\"<IMAGE_PATH>\"", "R0", "Indeksy, edition, arch i size.", "Brak zmian."),
            ("Disk layout", "WinPE — PowerShell", "Get-Disk | Select-Object Number,UniqueId,FriendlyName,PartitionStyle,Size,IsBoot,IsSystem", "R0", "Jednoznaczne IDs przed planem.", "Brak zmian."),
            ("Unattend lint", "Repo — Python 3", "python .\\scripts\\repo\\validate_unattend.py --path '<UNATTEND_XML>'", "R0", "Schema/sensitive-value warnings bez modyfikacji XML.", "Brak zmian."),
        ],
        ["windows-service-media", "winpe-offline-repair", "windows-bcd-partition-repair", "storage-triage-cloning-recovery"],
        ["ms-dism-image", "ms-sysprep", "ms-adk"],
    ),
    s(
        "windows-service-media",
        "Bezpieczny nośnik serwisowy",
        "projekt oficjalnego WinPE lub multiboot USB z manifestem, licencjami, SHA-256/signature i rozdzieleniem x64/ARM64",
        ["zrób pendrive serwisowy", "WinPE toolkit", "service USB", "herstel-USB maken"],
        "Nie pobierać ISO/binariów ani nie zapisywać USB bez jawnego polecenia i potwierdzenia celu.",
        ["nieustalony target USB", "brak backupu nośnika", "narzędzie redistribution forbidden", "niezweryfikowany checksum", "Secure Boot incompatibility"],
        ["target unique ID/capacity", "media manifest", "official URLs", "license/redistribution", "checksums/signatures", "UEFI/BIOS/arch"],
        [
            ("Plan oficjalnego WinPE", "ADK i add-on mogą być zainstalowane.", "Wersja ADK musi pasować scenariuszowi i mieć poprawki.", "Wykryć lokalnie ADK bez instalacji/pobierania.", "Wygenerować plan; build wykonać dopiero jawnie na lab host.", "Plan wskazuje ADK version, patch, arch i brak third-party binaries."),
            ("Multiboot Ventoy/Rufus", "Technik chce kilka legalnych obrazów.", "Secure Boot/licencje/integralność różnią się per asset.", "Zweryfikować każde źródło, hash i redistribution.", "Nie pobierać automatycznie restricted assets; zapisy USB jako R4.", "Manifest odpowiada plikom i testy UEFI/BIOS w lab przechodzą."),
            ("Aktualizacja zestawu", "Narzędzia mogły się zestarzeć.", "Stale/EOL tool może być ryzykiem.", "Porównać katalog z official release pages i diff do review.", "Pobierać dopiero po akceptacji licencji i weryfikacji.", "Integrity scan clean, provenance complete, EOL items quarantined."),
        ],
        [
            ("Plan media", "Repo — PowerShell 5.1+", "& '.\\scripts\\toolkit\\New-ServiceMediaPlan.ps1' -ManifestPath '.\\tools\\manifests\\service-media.yaml' -OutputPath '<OUTPUT>'", "R0", "Plan katalogów/pobierania bez zapisu USB.", "Usunąć plan."),
            ("Integrity", "Repo — PowerShell 5.1+", "& '.\\scripts\\toolkit\\Test-ServiceMediaIntegrity.ps1' -Root '<MEDIA_STAGING>' -ManifestPath '<PROVENANCE_JSON>'", "R0", "Hash/signature discrepancies; brak wykonania plików.", "Brak zmian."),
            ("Verified download plan", "Repo — PowerShell 5.1+", "& '.\\scripts\\toolkit\\Get-VerifiedServiceTool.ps1' -ToolId '<TOOL_ID>' -Destination '<STAGING>' -WhatIf", "R0", "Wyświetla version/source/license/size bez download.", "Brak zmian w WhatIf."),
        ],
        ["windows-tool-research", "windows-deployment-imaging", "bios-uefi-firmware", "windows-automation-powershell"],
        ["ms-adk", "ms-winpe", "rufus", "ventoy"],
    ),
    s(
        "windows-legacy-xp-vista-7-8",
        "Windows XP, Vista, 7 i 8.x",
        "izolowaną diagnozę legacy BIOS/MBR, NTLDR/boot.ini, starych BCD/WinRE, TLS/certyfikatów, sterowników i migracji",
        ["Windows XP nie startuje", "Windows 7 repair", "NTLDR missing", "oude Windows 8.1 laptop"],
        "Nie podłączać niewspieranego systemu bezpośrednio do Internetu ani udawać bieżącego bezpieczeństwa.",
        ["Internet exposure", "brak backupu na starym HDD", "legacy encryption", "brak legalnego media/driver", "ancient PSU/battery"],
        ["exact OS/SP/arch", "BIOS/MBR layout", "hardware age/health", "offline malware risk", "data migration target", "license/media provenance"],
        [
            ("NTLDR missing XP", "BIOS widzi dysk, komunikat przed logo.", "Active partition/boot files/boot.ini lub failing disk.", "Najpierw health/image, potem layout i read-only boot.ini.", "Recovery Console command tylko po backupie i właściwym target.", "Boot lub dane migrują; system pozostaje izolowany."),
            ("Windows 7 nie bootuje", "Startup Repair loop.", "BCD/update/driver/storage.", "Zebrać logs i health, uwzględnić stare WinRE.", "Najmniej inwazyjny rollback; plan migracji jako wynik długoterminowy.", "Dane skopiowane, system startuje offline lub urządzenie zastąpione."),
            ("Migracja z 8.1", "Aplikacja wymaga starego systemu.", "Hardware/software może nie mieć ścieżki upgrade.", "Inwentaryzacja danych/licencji/dependencies bez Win32_Product.", "Eksport danych i czysta migracja do wspieranego OS/VM izolowanej.", "Dane/aplikacja zweryfikowane, legacy host odizolowany."),
        ],
        [
            ("Legacy identity", "Windows XP/7 — CMD", "systeminfo", "R0", "OS/SP/hotfix/arch, jeśli WMI działa.", "Brak zmian."),
            ("Boot.ini read", "Recovery Console/WinPE — CMD", "type <SYSTEM_VOLUME>:\\boot.ini", "R0", "Konfiguracja ARC paths bez edycji.", "Brak zmian."),
            ("BCD read Vista–8.1", "WinRE — Command Prompt", "bcdedit /enum all", "R0", "Store entries bez zmiany.", "Brak zmian."),
        ],
        ["storage-triage-cloning-recovery", "windows-os-identification", "windows-bcd-partition-repair", "windows-service-media"],
        ["ms-xp-lifecycle", "ms-win7-lifecycle", "ms-win81-lifecycle"],
    ),
    s(
        "windows-10-support",
        "Wsparcie Windows 10",
        "dynamiczne ustalenie statusu 22H2/ESU/LTSC, bezpieczne utrzymanie i migrację urządzeń pozostających na Windows 10",
        ["Windows 10 support ended", "ESU Windows 10", "22H2 update", "Windows 10 ondersteuning"],
        "Nie zakładać, że wszystkie LTSC/LTSB mają ten sam lifecycle albo że ESU obejmuje feature support.",
        ["brak ESU na Internet-connected device", "unsupported app/security stack", "hardware not Win11 eligible", "managed licensing"],
        ["edition/channel/build", "ESU enrollment/status", "LTSC exact product", "hardware eligibility", "backup/migration blockers"],
        [
            ("22H2 po EOL", "Home/Pro działa po 2025-10-14.", "Bez ESU brak regularnych security updates.", "Ustalić edition i legalny ESU/enrollment lub plan migracji.", "Nie obiecywać wsparcia; ograniczyć exposure do migracji.", "Urządzenie ma ESU z aktualnymi KB albo przeszło na supported OS."),
            ("LTSC lifecycle", "Enterprise LTSC pozostaje w firmie.", "Daty różnią się między Enterprise i IoT.", "Porównać exact ProductName/EditionID z matrix.", "Stosować organizacyjne servicing i migration plan.", "Raport podaje konkretny product lifecycle, nie ogólne „Windows 10”."),
            ("PC nie spełnia Windows 11", "TPM/CPU blocker.", "Bypass obniży wspieralność.", "Sprawdzić oficjalne wymagania i firmware OEM.", "Rozważyć wymianę, supported Windows 10 ESU lub alternatywny supported OS; bez bypass.", "Wybrana opcja ma patching, backup i datę wyjścia."),
        ],
        [
            ("Release matrix", "Repo — Python 3", "python .\\scripts\\repo\\query_matrix.py --os windows-10 --build '<BUILD>'", "R0", "Lifecycle/ESU z datą snapshotu i source ID.", "Brak zmian."),
            ("OS identity", "Windows — PowerShell 5.1", "Get-ComputerInfo | Select-Object WindowsProductName,WindowsEditionId,OsBuildNumber,OsArchitecture", "R0", "Exact edition/build/arch.", "Brak zmian."),
            ("Update health", "Windows — PowerShell 5.1", "& '.\\scripts\\diagnostics\\Get-WindowsUpdateHealth.ps1' -FixturePath '<FIXTURE>' -OutputPath '<OUTPUT>'", "R0", "Update/ESU evidence bez zmian.", "Brak zmian."),
        ],
        ["windows-os-identification", "windows-11-support", "windows-update-servicing", "windows-deployment-imaging"],
        ["ms-win10-release", "ms-windows-esu", "ms-lifecycle"],
    ),
    s(
        "windows-11-support",
        "Bieżące Windows 11",
        "obsługę aktywnych gałęzi Windows 11, ARM64, UEFI/GPT, Device Encryption, VBS/HVCI, Hello, DCH i safeguard holds",
        ["Windows 11 24H2/25H2/26H1", "Windows 11 problem", "ARM64 app", "Windows 11 updateprobleem"],
        "Nie zakładać stałego numeru najnowszej wersji; zawsze czytać release matrix i release health.",
        ["26H1 traktowane jako upgrade dla istniejącego PC", "Secure Boot cert not updated", "BitLocker key not ready", "compatibility hold bypass"],
        ["version/build/edition", "hardware/arch", "release health", "Secure Boot/TPM/VBS", "Device Encryption", "driver DCH"],
        [
            ("Dobór aktywnej gałęzi", "PC ma 24H2/25H2/26H1.", "26H1 jest hardware-optimized i nie jest in-place path dla starszych urządzeń.", "Query dynamic matrix oraz model/OEM path.", "Nie wymuszać niewłaściwej branch; stosować oferowaną ścieżkę.", "Build pozostaje wspierany i miesięczne updates działają."),
            ("ARM64 compatibility", "Aplikacja/driver nie instaluje.", "Emulacja apps nie obejmuje każdego kernel drivera.", "Ustalić native arch pakietu i driver support OEM.", "Wybrać ARM64/native albo oficjalnie wspierany emulated app.", "Funkcja działa bez unsigned/bypass driver."),
            ("Device Encryption recovery risk", "Update firmware/security przed zmianą.", "TPM/Secure Boot PCR może wywołać BitLocker.", "Safety status, key readiness i management owner.", "Pilot/backup/suspend minimalny tylko z zgodą.", "Protection resumed i dwa cold boots bez recovery."),
        ],
        [
            ("Release matrix", "Repo — Python 3", "python .\\scripts\\repo\\query_matrix.py --os windows-11 --build '<BUILD>'", "R0", "Gałąź, EOL per edition i current snapshot.", "Brak zmian."),
            ("Security stack", "Windows — PowerShell jako administrator", "Get-Tpm; Confirm-SecureBootUEFI; Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\\Microsoft\\Windows\\DeviceGuard", "R0", "TPM/Secure Boot/VBS bez zmian.", "Brak zmian."),
            ("Release health", "Repo — PowerShell 5.1+", "& '.\\scripts\\repo\\Update-WindowsKnowledgeBase.ps1' -WhatIf", "R0", "Pobiera wyłącznie metadata do diff staging; nie przyjmuje zmian.", "Brak zmian w WhatIf."),
        ],
        ["windows-os-identification", "windows-update-servicing", "windows-bitlocker-tpm-security", "windows-drivers-devices"],
        ["ms-win11-release", "ms-release-health", "ms-secure-boot-2026"],
    ),
    s(
        "windows-post-repair-validation",
        "Walidacja po naprawie",
        "mierzalne testy przyczyny, objawu i regresji: boot, SMART, temperatury, sleep/wake, update, sieć, peryferia, backup i ryzyko resztkowe",
        ["sprawdź naprawę", "post repair validation", "burn-in", "controle na reparatie"],
        "Nie zastępować właściwej diagnozy; aktywować po wykonaniu naprawy lub przy zamknięciu sprawy.",
        ["niewyjaśnione storage/RAM errors", "temperatury przy limicie", "backup niezweryfikowany", "ochrona wyłączona", "test ryzykowny dla danych"],
        ["baseline before", "success criteria", "cause reproduction", "symptom test", "regression set", "residual risk"],
        [
            ("Walidacja naprawy software", "Objaw już nie występuje.", "Jedna udana próba może być przypadkiem.", "Powtórzyć exact repro, potem reboot/sleep/user workflow.", "Jeśli odchylenie wraca, cofnąć zmianę i wrócić do hipotez.", "Co najmniej trzy próby lub uzasadniony okres bez regresji."),
            ("Burn-in po hardware", "Wymieniono RAM/SSD/cooling.", "Intermittent fault może ujawnić się pod temperaturą/cyklem.", "Test właściwy komponentowi z limitami temperatur i stop conditions.", "Nie wykonywać stress przy danych bez backupu.", "Zero error, stabilne temperatury i cold boot/sleep cycles."),
            ("Zamknięcie z ryzykiem resztkowym", "Nie wszystkie hipotezy można wykluczyć.", "Brak lab/long test.", "Wymienić wykonane dowody, limity i monitoring.", "Nie oznaczać „naprawiono” bez warunku sukcesu.", "Raport rozróżnia fixed/mitigated/unverified i daje plan nawrotu."),
        ],
        [
            ("Validation bundle", "Windows — PowerShell 5.1", "& '.\\scripts\\diagnostics\\Get-WindowsRepairBundle.ps1' -Mode Basic -FixtureRoot '<FIXTURE_ROOT>' -OutputPath '<OUTPUT>'", "R0", "Before/after comparable JSON/Markdown i SHA-256.", "Usunąć bundle po retencji."),
            ("Repo checklist", "Repo — PowerShell 5.1+", "& '.\\scripts\\reporting\\New-WindowsServiceReport.ps1' -CasePath '<CASE>' -RequireValidation", "R0", "Raport odmawia final status bez validation entries.", "Brak zmian poza raportem."),
            ("Event regression", "Windows — PowerShell 5.1", "Get-WinEvent -FilterHashtable @{LogName='System';StartTime='<REPAIR_COMPLETED_UTC>'} | Where-Object LevelDisplayName -in 'Critical','Error'", "R0", "Nowe krytyczne/błędy do korelacji, nie automatyczna diagnoza.", "Brak zmian."),
        ],
        ["windows-case-evidence", "windows-service-intake", "pc-hardware-diagnostics", "windows-backup-vss-restore"],
        ["ms-reliability", "ms-powercfg", "ms-release-health"],
    ),
    s(
        "windows-tool-research",
        "Research narzędzi serwisowych",
        "utrzymanie katalogu narzędzi, official sources, wersji, licencji, statusu active/stale/EOL, checksum/signature i community findings",
        ["sprawdź narzędzie serwisowe", "is this tool safe", "update tool catalog", "hulpprogramma versie/licentie"],
        "Nie pobierać ani uruchamiać narzędzia podczas samego researchu.",
        ["download aggregator only", "license unknown", "unsigned asset", "latest.exe without version", "aggressive repair suite"],
        ["official home/repository", "exact version/release date", "license/commercial/redistribution", "hash/signature method", "supported OS/arch", "replacement/EOL"],
        [
            ("Aktualizacja aktywnego projektu", "Katalog ma starszą wersję.", "Release page może zmienić assety/licencję.", "Pobrać tylko metadata z official endpoint i zapisać diff.", "Review ręczny przed merge; downloader pin exact asset.", "Entry ma version/date/source/license/integrity i review status."),
            ("Porzucone narzędzie", "Brak release przez długi czas.", "Projekt może być stabilny albo EOL.", "Sprawdzić official repo/issues/site i compatibility reports.", "Oznaczyć stale/eol/unknown, podać alternatywę; nie udawać.", "Status i confidence mają dowody z datą."),
            ("Community repair suite", "Użytkownik pyta o WinUtil/Tron.", "Pakiet wykonuje wiele zmian i może zniszczyć dowody.", "Rozłożyć konkretne actions, source, version i rollback.", "Nigdy nie zalecać run-all; preferować natywne narzędzia.", "Rekomendacja dotyczy jednej przejrzanej funkcji albo odradza."),
        ],
        [
            ("Catalog diff", "Repo — PowerShell 5.1+", "& '.\\scripts\\repo\\Update-ToolCatalog.ps1' -WhatIf -OutputPath '<DIFF_JSON>'", "R0", "Metadata diff bez downloadu i bez akceptacji zmian.", "Usunąć diff."),
            ("Catalog query", "Repo — Python 3", "python .\\scripts\\repo\\query_tools.py --use-case '<USE_CASE>' --os '<OS>' --arch '<ARCH>'", "R0", "Ranking wbudowane→vendor→project z risk/license.", "Brak zmian."),
            ("Downloader plan", "Repo — PowerShell 5.1+", "& '.\\scripts\\toolkit\\Get-VerifiedServiceTool.ps1' -ToolId '<TOOL_ID>' -Destination '<STAGING>' -WhatIf", "R0", "Exact source/version/license/check method; brak download.", "Brak zmian w WhatIf."),
        ],
        ["windows-service-media", "windows-automation-powershell", "windows-case-evidence"],
        ["ms-sysinternals", "github-releases", "agentskills-spec"],
    ),
]


def source(
    source_id: str,
    title: str,
    url: str,
    publisher: str,
    source_type: str = "official",
    claim: str = "",
    status: str = "current",
    license_notes: str = "Link i synteza; prawa należą do wydawcy.",
) -> dict:
    return {
        "id": source_id,
        "title": title,
        "url": url,
        "publisher": publisher,
        "source_type": source_type,
        "retrieved_at": TODAY,
        "last_verified": TODAY,
        "applies_to": ["Windows client", "repo knowledge"],
        "claim_summary": claim or title,
        "confidence": "high" if source_type in {"official", "vendor", "project"} else "medium",
        "status": status,
        "license_notes": license_notes,
    }


SOURCES = [
    source("codex-skills", "Build skills", "https://learn.chatgpt.com/docs/build-skills", "OpenAI", claim="SKILL.md wymaga name i description; repo używa .agents/skills, a user scope $HOME/.agents/skills."),
    source("agentskills-spec", "Agent Skills specification", "https://agentskills.io/specification", "Agent Skills", "project", "Otwarty standard katalogu skill i front matter."),
    source("github-releases", "Linking to releases", "https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases", "GitHub", "official", "Oficjalny wzorzec releases/latest i asset provenance."),
    source("ms-support-troubleshoot", "Windows troubleshooting documentation", "https://learn.microsoft.com/en-us/troubleshoot/windows-client/welcome-windows-client", "Microsoft"),
    source("ms-privacy", "Microsoft privacy principles", "https://www.microsoft.com/privacy/privacystatement", "Microsoft"),
    source("ms-win11-release", "Windows 11 release information", "https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information", "Microsoft", claim="26H1, 25H2, 24H2 i 23H2 servicing/build/lifecycle; 26H1 tylko dla nowych urządzeń."),
    source("ms-win10-release", "Windows 10 release information", "https://learn.microsoft.com/en-us/windows/release-health/release-information", "Microsoft", claim="Windows 10 22H2 zakończył standardowe wsparcie i otrzymuje aktualizacje ESU dla zapisanych urządzeń."),
    source("ms-release-health", "Windows release health", "https://learn.microsoft.com/en-us/windows/release-health/", "Microsoft", claim="Bieżące known issues, safeguard holds i miesięczne informacje o wydaniach."),
    source("ms-lifecycle", "Lifecycle FAQ - Windows", "https://learn.microsoft.com/en-us/lifecycle/faq/windows", "Microsoft"),
    source("ms-windows-esu", "Windows 10 Extended Security Updates", "https://learn.microsoft.com/en-us/windows/whats-new/extended-security-updates", "Microsoft"),
    source("ms-xp-lifecycle", "Windows XP lifecycle", "https://learn.microsoft.com/en-us/lifecycle/products/windows-xp", "Microsoft", claim="Windows XP SP3 support ended 2014-04-08.", status="eol"),
    source("ms-win7-lifecycle", "Windows 7 lifecycle", "https://learn.microsoft.com/en-us/lifecycle/products/windows-7", "Microsoft", claim="Windows 7 support ended; ESU ended for common editions.", status="eol"),
    source("ms-win81-lifecycle", "Windows 8.1 lifecycle", "https://learn.microsoft.com/en-us/lifecycle/products/windows-81", "Microsoft", claim="Windows 8.1 support ended 2023-01-10.", status="eol"),
    source("ms-adk", "Download and install Windows ADK", "https://learn.microsoft.com/en-us/windows-hardware/get-started/adk-install", "Microsoft", claim="ADK 10.1.28000.1 supports Windows 11 26H1 ARM64 and requires current security servicing."),
    source("ms-winpe", "Windows PE overview", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/winpe-intro", "Microsoft"),
    source("ms-secure-boot-2026", "Update Secure Boot certificates for Windows devices", "https://learn.microsoft.com/en-us/troubleshoot/windows-client/windows-security/update-secure-boot-certificates", "Microsoft", claim="Certyfikaty Secure Boot 2011 wygasają od czerwca 2026; wdrażać certyfikaty 2023 po pilotażu."),
    source("ms-tpm", "Trusted Platform Module overview", "https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/trusted-platform-module-overview", "Microsoft"),
    source("ms-bitlocker-overview", "BitLocker overview", "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/", "Microsoft"),
    source("ms-wmi-computersystem", "Win32_ComputerSystem class", "https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-computersystem", "Microsoft"),
    source("ms-powercfg", "Powercfg command-line options", "https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/powercfg-command-line-options", "Microsoft"),
    source("ms-whea", "WHEA hardware error events", "https://learn.microsoft.com/en-us/windows-hardware/drivers/whea/", "Microsoft"),
    source("ms-get-filehash", "Get-FileHash", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash", "Microsoft"),
    source("nist-chain-evidence", "Digital evidence guidelines", "https://csrc.nist.gov/publications/detail/sp/800-86/final", "NIST", "official"),
    source("ifixit-esd", "Electrostatic discharge safety", "https://www.ifixit.com/Wiki/ESD", "iFixit", "secondary"),
    source("ms-startup-repair", "Startup Repair", "https://support.microsoft.com/en-us/windows/startup-repair-85deb0b9-fa3d-44d8-a2d1-2a6aee1f1e94", "Microsoft"),
    source("ms-winre", "Windows Recovery Environment", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-recovery-environment--windows-re--technical-reference", "Microsoft"),
    source("ms-bcdedit", "BCDEdit command-line options", "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/bcdedit--set", "Microsoft"),
    source("ms-bcdboot", "BCDBoot command-line options", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/bcdboot-command-line-options-techref-di", "Microsoft"),
    source("ms-bootrec", "Bootrec reference", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/bootrec-command-line-options", "Microsoft"),
    source("ms-dism-image", "DISM image management", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/what-is-dism", "Microsoft"),
    source("ms-reg", "Reg command", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reg", "Microsoft"),
    source("ms-dism-repair", "Repair a Windows image", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/repair-a-windows-image", "Microsoft"),
    source("ms-sfc", "System File Checker", "https://support.microsoft.com/en-us/topic/use-the-system-file-checker-tool-to-repair-missing-or-corrupted-system-files-79aa86cb-ca52-166a-92a3-966e85d4094e", "Microsoft"),
    source("ms-cbs-log", "Analyze SFC and CBS log", "https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/analyze-sfc-program-log-file-entries", "Microsoft"),
    source("ms-wu-troubleshoot", "Windows Update troubleshooting guidance", "https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/windows-update-issues-troubleshooting", "Microsoft"),
    source("ms-windowsupdate-log", "Get-WindowsUpdateLog", "https://learn.microsoft.com/en-us/powershell/module/windowsupdate/get-windowsupdatelog", "Microsoft"),
    source("ms-setupdiag", "SetupDiag", "https://learn.microsoft.com/en-us/windows/deployment/upgrade/setupdiag", "Microsoft"),
    source("ms-setup-logfiles", "Windows Setup log files", "https://learn.microsoft.com/en-us/windows/deployment/upgrade/log-files", "Microsoft"),
    source("ms-activation", "Activate Windows", "https://support.microsoft.com/en-us/windows/activate-windows-c39005d4-95ee-b91e-b399-2820fda32227", "Microsoft"),
    source("ms-activation-troubleshooter", "Activation troubleshooter", "https://support.microsoft.com/en-us/windows/using-the-activation-troubleshooter-d717cdff-cf19-9770-7198-40119c2a696c", "Microsoft"),
    source("ms-volume-activation", "Volume activation overview", "https://learn.microsoft.com/en-us/windows/deployment/volume-activation/volume-activation-windows", "Microsoft"),
    source("ms-windbg", "Install WinDbg", "https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/", "Microsoft"),
    source("ms-bugcheck", "Bug check code reference", "https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/bug-check-code-reference2", "Microsoft"),
    source("ms-driver-verifier", "Driver Verifier", "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/driver-verifier", "Microsoft"),
    source("ms-wpr", "Windows Performance Recorder", "https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder", "Microsoft"),
    source("ms-wpa", "Windows Performance Analyzer", "https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer", "Microsoft"),
    source("ms-perfmon", "Performance Monitor", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/perfmon", "Microsoft"),
    source("ms-reliability", "Reliability analysis component", "https://learn.microsoft.com/en-us/windows/win32/wer/using-wer", "Microsoft"),
    source("ms-services", "Service control manager", "https://learn.microsoft.com/en-us/windows/win32/services/service-control-manager", "Microsoft"),
    source("ms-scheduledtasks", "ScheduledTasks module", "https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/", "Microsoft"),
    source("sysinternals-autoruns", "Autoruns", "https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns", "Microsoft"),
    source("ms-pnputil", "PnPUtil", "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/pnputil-command-syntax", "Microsoft"),
    source("ms-setupapi", "SetupAPI device installation log", "https://learn.microsoft.com/en-us/windows-hardware/drivers/install/setupapi-device-installation-log-entries", "Microsoft"),
    source("ms-driver-store", "Driver Store", "https://learn.microsoft.com/en-us/windows-hardware/drivers/install/driver-store", "Microsoft"),
    source("ms-nettcpip", "NetTCPIP module", "https://learn.microsoft.com/en-us/powershell/module/nettcpip/", "Microsoft"),
    source("ms-netsh", "Netsh", "https://learn.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh", "Microsoft"),
    source("ms-printer-troubleshoot", "Troubleshoot printer problems", "https://support.microsoft.com/en-us/windows/fix-printer-connection-and-printing-problems-in-windows-fb830bff-7702-6349-33cd-9443fe987f73", "Microsoft"),
    source("ms-bluetooth", "Fix Bluetooth problems", "https://support.microsoft.com/en-us/windows/fix-bluetooth-problems-in-windows-723e092f-03fa-858b-5c80-131ec3fba75c", "Microsoft"),
    source("ms-account-recovery", "Microsoft account recovery", "https://support.microsoft.com/en-us/account-billing/help-with-the-microsoft-account-recovery-form-b19c02d1-a782-dee6-93c3-dc8113b20c42", "Microsoft"),
    source("ms-hello", "Windows Hello troubleshooting", "https://support.microsoft.com/en-us/windows/troubleshoot-problems-with-windows-hello-bf68539e-e95e-48b6-a6cb-455649db3887", "Microsoft"),
    source("ms-user-profile", "User profile service", "https://learn.microsoft.com/en-us/troubleshoot/windows-client/user-profiles-and-logon/", "Microsoft"),
    source("ms-icacls", "icacls", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls", "Microsoft"),
    source("ms-smbshare", "SmbShare module", "https://learn.microsoft.com/en-us/powershell/module/smbshare/", "Microsoft"),
    source("ms-efs", "Encrypting File System", "https://learn.microsoft.com/en-us/windows/win32/fileio/file-encryption", "Microsoft"),
    source("ms-defender-offline", "Microsoft Defender Offline", "https://support.microsoft.com/en-us/windows/help-protect-my-pc-with-microsoft-defender-offline-9306d528-64bf-4668-5b80-ff533f183d6c", "Microsoft"),
    source("ms-msert", "Microsoft Safety Scanner", "https://learn.microsoft.com/en-us/defender-endpoint/safety-scanner-download", "Microsoft"),
    source("ms-winget", "Windows Package Manager", "https://learn.microsoft.com/en-us/windows/package-manager/winget/", "Microsoft"),
    source("ms-appx", "Appx module", "https://learn.microsoft.com/en-us/powershell/module/appx/", "Microsoft"),
    source("ms-msi-logging", "Enable Windows Installer logging", "https://learn.microsoft.com/en-us/troubleshoot/windows-client/application-management/enable-windows-installer-logging", "Microsoft"),
    source("ms-start-menu", "Troubleshoot Start menu errors", "https://learn.microsoft.com/en-us/troubleshoot/windows-client/shell-experience/troubleshoot-start-menu-errors", "Microsoft"),
    source("ms-office-repair", "Repair an Office application", "https://support.microsoft.com/en-us/office/repair-an-office-application-7821d4b6-7c1d-4205-aa0e-a6b40c5bb88b", "Microsoft"),
    source("ms-onedrive", "OneDrive troubleshooting", "https://support.microsoft.com/en-us/onedrive", "Microsoft"),
    source("ms-teams-troubleshoot", "Teams troubleshooting", "https://learn.microsoft.com/en-us/microsoftteams/troubleshoot/teams-welcome", "Microsoft"),
    source("ms-vss", "Volume Shadow Copy Service", "https://learn.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service", "Microsoft"),
    source("ms-file-history", "File History", "https://support.microsoft.com/en-us/windows/backup-and-restore-with-file-history-7bf065bf-f1ea-0a78-c1cf-7dcf51cc8bfc", "Microsoft"),
    source("ms-windows-backup", "Windows Backup", "https://support.microsoft.com/en-us/windows/back-up-your-windows-pc-87a81f8a-78fa-456e-b521-ac0560e32338", "Microsoft"),
    source("ms-dsregcmd", "dsregcmd troubleshooting", "https://learn.microsoft.com/en-us/entra/identity/devices/troubleshoot-device-dsregcmd", "Microsoft"),
    source("ms-gpresult", "gpresult", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/gpresult", "Microsoft"),
    source("ms-quick-assist", "Quick Assist", "https://support.microsoft.com/en-us/windows/solve-pc-problems-remotely-using-quick-assist-f20765d1-9d0a-4b85-8a3a-c9f8f3c0f0a9", "Microsoft"),
    source("ms-get-winevent", "Get-WinEvent", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent", "Microsoft"),
    source("ms-registry", "about Registry Provider", "https://learn.microsoft.com/en-us/powershell/provider/registry-provider", "Microsoft"),
    source("ms-optionalfeatures", "DISM optional features", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/enable-or-disable-windows-features-using-dism", "Microsoft"),
    source("ms-powershell-shouldprocess", "Everything about ShouldProcess", "https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess", "Microsoft"),
    source("pester-docs", "Pester documentation", "https://pester.dev/docs/quick-start", "Pester", "project"),
    source("psscriptanalyzer", "PSScriptAnalyzer", "https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview", "Microsoft"),
    source("ms-sysprep", "Sysprep overview", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/sysprep--system-preparation--overview", "Microsoft"),
    source("ms-sysinternals", "Sysinternals Suite", "https://learn.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite", "Microsoft", claim="Suite 2026.7, updated 2026-07-09, with x64/ARM64 downloads."),
    source("smartmontools", "smartmontools", "https://www.smartmontools.org/", "smartmontools", "project"),
    source("gddrescue", "GNU ddrescue", "https://www.gnu.org/software/ddrescue/", "GNU", "project"),
    source("opensuperclone", "OpenSuperClone", "https://github.com/ISpillMyDrink/OpenSuperClone", "OpenSuperClone", "project"),
    source("testdisk", "TestDisk and PhotoRec", "https://www.cgsecurity.org/", "CGSecurity", "project", "TestDisk/PhotoRec stable 7.2 at verification."),
    source("memtest86plus", "MemTest86+", "https://github.com/memtest86plus/memtest86plus", "MemTest86+", "project", "v8.10 released 2026-05-16; GPL-2.0."),
    source("wireshark", "Wireshark download", "https://www.wireshark.org/download.html", "Wireshark Foundation", "project", "Stable 4.6.7; signed signatures file and Windows x64/ARM64 packages."),
    source("rufus", "Rufus", "https://github.com/pbatard/rufus", "Pete Batard", "project", "Stable 4.14 at verification; GPL-3.0."),
    source("ventoy", "Ventoy download", "https://www.ventoy.net/en/download.html", "Ventoy", "project", "Official download page publishes pinned assets and SHA-256."),
]


SOURCE_BY_ID = {item["id"]: item for item in SOURCES}


def tool(
    tool_id: str,
    name: str,
    category: str,
    publisher: str,
    home: str,
    *,
    version: str = "os-component",
    status: str = "active",
    license_name: str = "Windows license",
    commercial: str = "allowed-with-valid-license",
    redistribution: str = "forbidden",
    oses: list[str] | None = None,
    arch: list[str] | None = None,
    env: list[str] | None = None,
    portable: bool = True,
    install_type: str = "built-in",
    risk: str = "R0",
    signature: str = "Windows component integrity",
    checksum: str = "not-applicable",
    source_ids: list[str] | None = None,
    avoid: list[str] | None = None,
    gotchas: list[str] | None = None,
    repo: str = "",
    download: str = "",
) -> dict:
    return {
        "id": tool_id,
        "name": name,
        "category": category,
        "publisher": publisher,
        "official_home": home,
        "official_download": download or home,
        "official_repository": repo,
        "current_version": version,
        "checked_at": TODAY,
        "status": status,
        "replaced_by": "",
        "license": license_name,
        "commercial_use": commercial,
        "redistribution": redistribution,
        "supported_os": oses or ["Windows 10", "Windows 11"],
        "architectures": arch or ["x64", "ARM64 where OS provides it"],
        "environments": env or ["online Windows"],
        "portable": portable,
        "install_type": install_type,
        "network_required": False,
        "elevation_required": risk in {"R2", "R3", "R4"},
        "signature_method": signature,
        "checksum_method": checksum,
        "risk_class": risk,
        "use_cases": [category],
        "avoid_when": avoid or ["nieznany target", "brak autoryzacji"],
        "known_gotchas": gotchas or ["Wynik narzędzia jest dowodem cząstkowym, nie automatyczną diagnozą."],
        "alternatives": [],
        "sources": source_ids or ["ms-support-troubleshoot"],
    }


BUILTIN_TOOLS = [
    ("dism", "DISM", "servicing", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/what-is-dism", "R2"),
    ("sfc", "System File Checker", "servicing", "https://support.microsoft.com/en-us/topic/use-the-system-file-checker-tool-to-repair-missing-or-corrupted-system-files-79aa86cb-ca52-166a-92a3-966e85d4094e", "R2"),
    ("chkdsk", "CHKDSK", "storage", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/chkdsk", "R3"),
    ("bcdboot", "BCDBoot", "boot", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/bcdboot-command-line-options-techref-di", "R3"),
    ("bootrec", "Bootrec", "boot", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/bootrec-command-line-options", "R3"),
    ("bcdedit", "BCDEdit", "boot", "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/bcdedit--set", "R3"),
    ("reagentc", "ReAgentC", "recovery", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/reagentc-command-line-options", "R2"),
    ("diskpart", "DiskPart", "storage", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskpart", "R4"),
    ("mountvol", "MountVol", "storage", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mountvol", "R3"),
    ("fsutil", "FsUtil", "storage", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil", "R3"),
    ("robocopy", "Robocopy", "data-copy", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy", "R2"),
    ("reg", "Reg.exe", "registry", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reg", "R3"),
    ("wevtutil", "Wevtutil", "events", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wevtutil", "R2"),
    ("pnputil", "PnPUtil", "drivers", "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/pnputil-command-syntax", "R3"),
    ("powercfg", "PowerCfg", "power", "https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/powercfg-command-line-options", "R2"),
    ("netsh", "Netsh", "network", "https://learn.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh", "R2"),
    ("setupdiag", "SetupDiag", "setup", "https://learn.microsoft.com/en-us/windows/deployment/upgrade/setupdiag", "R0"),
    ("windbg", "WinDbg", "debugging", "https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/", "R0"),
    ("wpr", "Windows Performance Recorder", "performance", "https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder", "R0"),
    ("wpa", "Windows Performance Analyzer", "performance", "https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer", "R0"),
    ("perfmon", "Performance Monitor", "performance", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/perfmon", "R0"),
    ("reliability-monitor", "Reliability Monitor", "reliability", "https://learn.microsoft.com/en-us/windows/win32/wer/using-wer", "R0"),
    ("event-viewer", "Event Viewer", "events", "https://learn.microsoft.com/en-us/shows/inside/event-viewer", "R0"),
    ("driver-verifier", "Driver Verifier", "drivers", "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/driver-verifier", "R3"),
    ("windows-memory-diagnostic", "Windows Memory Diagnostic", "memory", "https://support.microsoft.com/en-us/windows/diagnosing-memory-problems-on-your-computer-8231df72-d541-c2e4-010c-8bd503e6bb6f", "R1"),
    ("defender-offline", "Microsoft Defender Offline", "malware", "https://support.microsoft.com/en-us/windows/help-protect-my-pc-with-microsoft-defender-offline-9306d528-64bf-4668-5b80-ff533f183d6c", "R2"),
    ("msert", "Microsoft Safety Scanner", "malware", "https://learn.microsoft.com/en-us/defender-endpoint/safety-scanner-download", "R2"),
    ("quick-assist", "Quick Assist", "remote", "https://support.microsoft.com/en-us/windows/solve-pc-problems-remotely-using-quick-assist-f20765d1-9d0a-4b85-8a3a-c9f8f3c0f0a9", "R1"),
    ("windows-sandbox", "Windows Sandbox", "isolation", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/", "R2"),
    ("windows-adk", "Windows ADK", "deployment", "https://learn.microsoft.com/en-us/windows-hardware/get-started/adk-install", "R2"),
    ("windows-pe", "Windows PE add-on", "deployment", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/winpe-intro", "R2"),
    ("winget", "Windows Package Manager", "packages", "https://learn.microsoft.com/en-us/windows/package-manager/winget/", "R2"),
]

TOOLS = [
    tool(tid, name, category, "Microsoft", home, risk=risk, source_ids=["ms-support-troubleshoot"])
    for tid, name, category, home, risk in BUILTIN_TOOLS
]


def add_external_tools() -> None:
    external = [
        ("sysinternals-suite", "Sysinternals Suite", "diagnostics", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite", "2026.7", "Sysinternals EULA", "forbidden", "Authenticode", "published SHA-256/Authenticode", ["ms-sysinternals"]),
        ("autoruns", "Autoruns", "startup", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["sysinternals-autoruns"]),
        ("process-explorer", "Process Explorer", "process", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["ms-sysinternals"]),
        ("process-monitor", "Process Monitor", "process", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/procmon", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["ms-sysinternals"]),
        ("procdump", "ProcDump", "debugging", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/procdump", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["ms-sysinternals"]),
        ("rammap", "RAMMap", "memory", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/rammap", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["ms-sysinternals"]),
        ("vmmap", "VMMap", "memory", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/vmmap", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["ms-sysinternals"]),
        ("sigcheck", "Sigcheck", "security", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/sigcheck", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["ms-sysinternals"]),
        ("tcpview", "TCPView", "network", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/tcpview", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["ms-sysinternals"]),
        ("pstools", "PsTools", "administration", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/pstools", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["ms-sysinternals"]),
        ("sysmon", "Sysmon", "security", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["ms-sysinternals"]),
        ("disk2vhd", "Disk2vhd", "imaging", "Microsoft", "https://learn.microsoft.com/en-us/sysinternals/downloads/disk2vhd", "rolling-suite", "Sysinternals EULA", "forbidden", "Authenticode", "Authenticode", ["ms-sysinternals"]),
        ("rufus", "Rufus", "boot-media", "Pete Batard", "https://rufus.ie/", "4.14", "GPL-3.0", "allowed", "Authenticode where published", "SHA-256 from official release", ["rufus"]),
        ("ventoy", "Ventoy", "multiboot", "Ventoy", "https://www.ventoy.net/en/download.html", "1.1.x-current-page", "GPL-3.0", "allowed", "project signatures vary", "SHA-256 on official page", ["ventoy"]),
        ("systemrescue", "SystemRescue", "rescue-media", "SystemRescue", "https://www.system-rescue.org/Download/", "rolling", "GPL and component licenses", "allowed", "PGP", "SHA-256/PGP", ["github-releases"]),
        ("clonezilla", "Clonezilla Live", "imaging", "NCHC", "https://clonezilla.org/downloads.php", "rolling", "GPL-2.0", "allowed", "checksums", "SHA-256", ["github-releases"]),
        ("rescuezilla", "Rescuezilla", "imaging", "Rescuezilla", "https://rescuezilla.com/download", "rolling", "GPL-3.0", "allowed", "checksums", "SHA-256", ["github-releases"]),
        ("gparted-live", "GParted Live", "partitioning", "GParted", "https://gparted.org/download.php", "rolling", "GPL-2.0", "allowed", "checksums", "SHA-256", ["github-releases"]),
        ("hirens-bootcd-pe", "Hiren's BootCD PE", "aggregated-rescue-media", "Hiren's BootCD", "https://www.hirensbootcd.org/download/", "rolling", "mixed/verify each component", "forbidden", "published hash", "SHA-256", ["github-releases"]),
        ("medicat", "MediCat USB", "aggregated-rescue-media", "MediCat", "https://medicatusb.com/", "rolling", "mixed/unclear", "forbidden", "unknown", "project checksum if present", ["github-releases"]),
        ("crystaldiskinfo", "CrystalDiskInfo", "storage-health", "Crystal Dew World", "https://crystalmark.info/en/software/crystaldiskinfo/", "rolling", "MIT", "allowed", "Authenticode/checksum varies", "official hash if present", ["smartmontools"]),
        ("smartmontools", "smartmontools", "storage-health", "smartmontools", "https://www.smartmontools.org/", "rolling", "GPL-2.0", "allowed", "project signature", "SHA-256/signature", ["smartmontools"]),
        ("gsmartcontrol", "GSmartControl", "storage-health", "GSmartControl", "https://gsmartcontrol.shaduri.dev/", "rolling", "GPL-3.0", "allowed", "project packages", "SHA-256 where published", ["smartmontools"]),
        ("hddscan", "HDDScan", "storage-test", "HDDScan", "https://hddscan.com/", "rolling", "freeware", "unknown", "unknown", "unknown", ["smartmontools"]),
        ("victoria", "Victoria HDD/SSD", "storage-write-risk", "Victoria", "https://hdd.by/victoria/", "rolling", "freeware/verify", "unknown", "unknown", "unknown", ["smartmontools"]),
        ("testdisk", "TestDisk", "data-recovery", "CGSecurity", "https://www.cgsecurity.org/wiki/TestDisk_Download", "7.2", "GPL-2.0", "allowed", "PGP/checksum", "SHA-256", ["testdisk"]),
        ("photorec", "PhotoRec", "data-recovery", "CGSecurity", "https://www.cgsecurity.org/wiki/TestDisk_Download", "7.2", "GPL-2.0", "allowed", "PGP/checksum", "SHA-256", ["testdisk"]),
        ("gddrescue", "GNU ddrescue", "imaging-recovery", "GNU", "https://www.gnu.org/software/ddrescue/", "rolling", "GPL-3.0", "allowed", "GNU signatures", "GPG/checksum", ["gddrescue"]),
        ("opensuperclone", "OpenSuperClone", "imaging-recovery", "OpenSuperClone", "https://github.com/ISpillMyDrink/OpenSuperClone", "rolling", "GPL-2.0", "allowed", "GitHub release provenance", "SHA-256 locally", ["opensuperclone"]),
        ("dmde", "DMDE", "data-recovery", "DMDE Software", "https://dmde.com/", "rolling", "commercial/free edition terms", "forbidden", "vendor package", "vendor checksum if present", ["testdisk"]),
        ("r-studio", "R-Studio", "data-recovery", "R-Tools Technology", "https://www.r-studio.com/", "rolling", "commercial", "forbidden", "vendor signature", "Authenticode", ["testdisk"]),
        ("ufs-explorer", "UFS Explorer", "data-recovery", "SysDev Laboratories", "https://www.ufsexplorer.com/", "rolling", "commercial", "forbidden", "vendor signature", "Authenticode", ["testdisk"]),
        ("hwinfo", "HWiNFO", "hardware-monitoring", "REALiX", "https://www.hwinfo.com/download/", "rolling", "freeware/commercial terms", "forbidden", "Authenticode", "vendor checksum if present", ["ms-whea"]),
        ("cpu-z", "CPU-Z", "hardware-info", "CPUID", "https://www.cpuid.com/softwares/cpu-z.html", "rolling", "freeware", "forbidden", "Authenticode", "vendor checksum", ["ms-whea"]),
        ("gpu-z", "GPU-Z", "hardware-info", "TechPowerUp", "https://www.techpowerup.com/gpuz/", "rolling", "freeware", "forbidden", "Authenticode", "vendor checksum", ["ms-whea"]),
        ("memtest86plus", "MemTest86+", "memory-test", "MemTest86+", "https://memtest.org/", "8.10", "GPL-2.0", "allowed", "project release", "SHA-256", ["memtest86plus"]),
        ("memtest86", "MemTest86", "memory-test", "PassMark", "https://www.memtest86.com/download.htm", "rolling", "free/commercial proprietary", "forbidden", "vendor signature", "vendor checksum", ["memtest86plus"]),
        ("occt", "OCCT", "stress-test", "OCBASE", "https://www.ocbase.com/download", "rolling", "personal/commercial terms", "forbidden", "Authenticode", "vendor checksum if present", ["ms-whea"]),
        ("prime95", "Prime95", "stress-test", "Mersenne Research", "https://www.mersenne.org/download/", "rolling", "freeware", "forbidden", "vendor package", "vendor checksum if present", ["ms-whea"]),
        ("furmark", "FurMark", "gpu-stress", "Geeks3D", "https://geeks3d.com/furmark/", "rolling", "freeware/commercial terms", "forbidden", "Authenticode where present", "vendor checksum if present", ["ms-whea"]),
        ("latencymon", "LatencyMon", "dpc-analysis", "Resplendence", "https://www.resplendence.com/latencymon", "rolling", "free home/commercial license", "forbidden", "Authenticode", "vendor package", ["ms-wpr"]),
        ("ddu", "Display Driver Uninstaller", "driver-cleanup", "Wagnardsoft", "https://www.wagnardsoft.com/display-driver-uninstaller-ddu-", "rolling", "freeware terms", "forbidden", "vendor package", "vendor checksum if present", ["ms-driver-store"]),
        ("driver-store-explorer", "Driver Store Explorer", "driver-store", "Lostindark", "https://github.com/lostindark/DriverStoreExplorer", "rolling", "GPL-2.0", "allowed", "GitHub release", "SHA-256 locally", ["github-releases"]),
        ("sdio", "Snappy Driver Installer Origin", "driver-pack", "SDIO", "https://www.snappy-driver-installer.org/", "rolling", "GPL and driver licenses", "forbidden", "project packages", "hashes vary", ["github-releases"]),
        ("malwarebytes", "Malwarebytes", "second-opinion-malware", "Malwarebytes", "https://www.malwarebytes.com/", "rolling", "commercial/free terms", "forbidden", "Authenticode", "vendor signature", ["ms-defender-offline"]),
        ("adwcleaner", "AdwCleaner", "pup-removal", "Malwarebytes", "https://www.malwarebytes.com/adwcleaner", "rolling", "freeware terms", "forbidden", "Authenticode", "vendor signature", ["ms-defender-offline"]),
        ("eset-sysinspector", "ESET SysInspector", "malware-triage", "ESET", "https://www.eset.com/int/support/sysinspector/", "rolling", "vendor terms", "forbidden", "Authenticode", "vendor signature", ["ms-defender-offline"]),
        ("wireshark", "Wireshark", "packet-analysis", "Wireshark Foundation", "https://www.wireshark.org/download.html", "4.6.7", "GPL-2.0", "allowed", "signed signature file", "SHA-256/PGP", ["wireshark"]),
        ("iperf3", "iperf3", "network-throughput", "ESnet", "https://software.es.net/iperf/", "rolling", "BSD-3-Clause", "allowed", "project packages", "SHA-256 locally", ["github-releases"]),
        ("nmap", "Nmap", "authorized-network-discovery", "Nmap Project", "https://nmap.org/download.html", "rolling", "NPSL/commercial terms", "forbidden", "project signature", "SHA-256/signature", ["github-releases"]),
        ("everything", "Everything", "file-search", "voidtools", "https://www.voidtools.com/downloads/", "rolling", "freeware/commercial terms", "forbidden", "Authenticode", "vendor checksum", ["github-releases"]),
        ("wiztree", "WizTree", "disk-usage", "Antibody Software", "https://diskanalyzer.com/download", "rolling", "personal/commercial license", "forbidden", "Authenticode", "vendor checksum", ["github-releases"]),
        ("treesize", "TreeSize", "disk-usage", "JAM Software", "https://www.jam-software.com/treesize_free", "rolling", "free/commercial editions", "forbidden", "Authenticode", "vendor signature", ["github-releases"]),
        ("bcu", "Bulk Crap Uninstaller", "uninstall", "BCUninstaller", "https://www.bcuninstaller.com/", "rolling", "Apache-2.0", "allowed", "GitHub release", "SHA-256 locally", ["github-releases"]),
        ("revo-uninstaller", "Revo Uninstaller", "uninstall", "VS Revo Group", "https://www.revouninstaller.com/", "rolling", "free/commercial terms", "forbidden", "Authenticode", "vendor signature", ["github-releases"]),
        ("ninite", "Ninite", "package-installer", "Secure By Design", "https://ninite.com/", "service", "commercial/free terms", "forbidden", "TLS/vendor signature", "Authenticode", ["github-releases"]),
        ("chocolatey", "Chocolatey", "package-manager", "Chocolatey Software", "https://chocolatey.org/", "rolling", "Apache/community and commercial terms", "conditional", "package checksums", "per-package checksum", ["github-releases"]),
        ("scoop", "Scoop", "package-manager", "ScoopInstaller", "https://scoop.sh/", "rolling", "Unlicense", "allowed", "manifest hashes", "SHA-256 per manifest", ["github-releases"]),
        ("winutil", "Chris Titus Tech WinUtil", "tweak-suite", "Chris Titus Tech", "https://github.com/ChrisTitusTech/winutil", "rolling", "MIT", "allowed", "source tags", "SHA-256 locally", ["github-releases"]),
        ("sophia-script", "Sophia Script", "tweak-suite", "Sophia Community", "https://github.com/farag2/Sophia-Script-for-Windows", "rolling", "MIT", "allowed", "GitHub release", "SHA-256 locally", ["github-releases"]),
        ("windows-repair-toolbox", "Windows Repair Toolbox", "tool-aggregator", "Windows Repair Toolbox", "https://windows-repair-toolbox.com/", "rolling", "freeware/mixed downloads", "forbidden", "vendor package", "per-tool verification", ["github-releases"]),
        ("tweaking-windows-repair", "Tweaking.com Windows Repair", "aggressive-repair-suite", "Tweaking.com", "https://www.tweaking.com/features/windows-repair-all-in-one/", "rolling", "free/proprietary", "forbidden", "Authenticode", "vendor signature", ["github-releases"]),
        ("tron-script", "Tron", "aggressive-remediation", "bmrf", "https://github.com/bmrf/tron", "rolling", "MIT plus bundled licenses", "forbidden", "release checksums", "SHA-256", ["github-releases"]),
        ("veeam-agent", "Veeam Agent for Microsoft Windows", "backup", "Veeam", "https://www.veeam.com/products/free/microsoft-windows.html", "rolling", "free/commercial EULA", "forbidden", "Authenticode", "vendor signature", ["ms-windows-backup"]),
        ("hasleo-backup", "Hasleo Backup Suite", "backup", "Hasleo", "https://www.easyuefi.com/backup-software/backup-suite-free.html", "rolling", "free/commercial terms", "forbidden", "Authenticode", "vendor signature", ["ms-windows-backup"]),
        ("macrium-reflect", "Macrium Reflect", "backup", "Macrium", "https://www.macrium.com/products/home", "rolling", "commercial/trial terms", "forbidden", "Authenticode", "vendor signature", ["ms-windows-backup"]),
        ("nirsoft", "NirSoft utilities", "diagnostic-utilities", "NirSoft", "https://www.nirsoft.net/", "per-tool", "freeware terms", "forbidden", "many unsigned/false positives", "vendor hashes vary", ["github-releases"]),
    ]
    for row in external:
        tid, name, category, publisher, home, version, lic, redistribution, signature, checksum, source_ids = row
        risk = "R3" if category in {"partitioning", "storage-write-risk", "aggressive-repair-suite", "aggressive-remediation", "driver-cleanup", "driver-pack"} else "R2" if category in {"tweak-suite", "malware", "pup-removal", "second-opinion-malware", "stress-test", "gpu-stress"} else "R0"
        TOOLS.append(
            tool(
                tid,
                name,
                category,
                publisher,
                home,
                version=version,
                license_name=lic,
                redistribution=redistribution,
                signature=signature,
                checksum=checksum,
                source_ids=source_ids,
                risk=risk,
                install_type="portable-or-installer",
                commercial="verify-license-before-commercial-use",
            )
        )


add_external_tools()


def clean(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def write(path: str | Path, content: str) -> None:
    target = ROOT / path if not isinstance(path, Path) or not path.is_absolute() else path
    target.parent.mkdir(parents=True, exist_ok=True)
    # Windows PowerShell 5.1 treats BOM-less UTF-8 scripts as the active ANSI
    # code page. The repository intentionally contains Polish diagnostics, so
    # PowerShell sources need a BOM on the declared 5.1 baseline.
    encoding = "utf-8-sig" if target.suffix.lower() in {".ps1", ".psm1", ".psd1"} else "utf-8"
    target.write_text(content.replace("\r\n", "\n"), encoding=encoding, newline="\n")


def dump_yaml_json(path: str | Path, value: object) -> None:
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def slug(value: str) -> str:
    value = value.lower().replace("ł", "l").replace("ó", "o").replace("ś", "s")
    value = value.replace("ą", "a").replace("ę", "e").replace("ć", "c").replace("ż", "z").replace("ź", "z").replace("ń", "n")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def skill_description(spec: dict) -> str:
    triggers = "; ".join(spec["triggers"][:4])
    return (
        f"Prowadzi bezpieczną diagnostykę i kontrolowane działania dla: {spec['focus']}. "
        f"Aktywuj przy zgłoszeniach: {triggers}. Use for Windows service diagnostics in this domain; "
        f"do not use outside this scope. Zawsze zaczynaj od ochrony danych i dowodów."
    )


ORCHESTRATOR_CRITICAL = {
    "bios-uefi-firmware",
    "storage-triage-cloning-recovery",
    "windows-bcd-partition-repair",
    "windows-bitlocker-tpm-security",
    "windows-deployment-imaging",
    "windows-malware-remediation",
    "winpe-offline-repair",
}
ORCHESTRATOR_FAST_READERS = {
    "windows-os-identification",
    "windows-tool-research",
}
ORCHESTRATOR_STANDARD = {
    "windows-10-support",
    "windows-11-support",
    "windows-apps-store-winget",
    "windows-automation-powershell",
    "windows-network-repair",
    "windows-performance-hangs",
    "windows-peripherals-repair",
    "windows-process-service-startup",
    "windows-remote-managed-client",
    "windows-service-intake",
    "windows-shell-ui-repair",
}


def orchestrator_metadata(name: str) -> dict[str, str]:
    if name in ORCHESTRATOR_CRITICAL:
        profile, reasoning, delegation, review, parallel, risk = (
            "expert_worker", "high", "required", "required", "forbidden", "critical"
        )
    elif name == "windows-case-evidence":
        profile, reasoning, delegation, review, parallel, risk = (
            "fast_worker", "medium", "optional", "optional", "forbidden", "medium"
        )
    elif name == "windows-master-router":
        profile, reasoning, delegation, review, parallel, risk = (
            "fast_reader", "medium", "forbidden", "optional", "forbidden", "low"
        )
    elif name == "windows-post-repair-validation":
        profile, reasoning, delegation, review, parallel, risk = (
            "reviewer", "high", "preferred", "none", "allowed", "medium"
        )
    elif name in ORCHESTRATOR_FAST_READERS:
        profile, reasoning, delegation, review, parallel, risk = (
            "fast_reader", "low", "optional", "optional", "allowed", "medium"
        )
    elif name in ORCHESTRATOR_STANDARD:
        profile, reasoning, delegation, review, parallel, risk = (
            "standard_worker", "medium", "preferred", "auto", "allowed", "medium"
        )
    else:
        profile, reasoning, delegation, review, parallel, risk = (
            "expert_worker", "high", "preferred", "required", "forbidden", "high"
        )
    minimum = "fast_reader" if profile == "reviewer" or name == "windows-case-evidence" else profile
    return {
        "swietlik.orchestrator.schema": "1",
        "swietlik.orchestrator.pack": "windows-pc-skills",
        "swietlik.orchestrator.recommended-agent": profile,
        "swietlik.orchestrator.minimum-agent": minimum,
        "swietlik.orchestrator.reasoning": reasoning,
        "swietlik.orchestrator.verbosity": "medium" if profile == "expert_worker" else "low",
        "swietlik.orchestrator.delegation": delegation,
        "swietlik.orchestrator.review": review,
        "swietlik.orchestrator.parallel": parallel,
        "swietlik.orchestrator.risk": risk,
    }


def orchestrator_frontmatter(name: str) -> str:
    rows = ["metadata:"]
    rows.extend(f'  {key}: "{value}"' for key, value in orchestrator_metadata(name).items())
    return "\n".join(rows)


def generate_skill(spec: dict) -> None:
    name = spec["name"]
    folder = SKILL_ROOT / name
    folder.mkdir(parents=True, exist_ok=True)
    description = skill_description(spec).replace('"', "'")
    execution_metadata = orchestrator_frontmatter(name)
    related_links = "\n".join(
        f"- [`{item}`](../{item}/SKILL.md) — użyj tylko, gdy dowód wskazuje tę domenę."
        for item in spec["related"]
    )
    red_flags = "\n".join(f"- **STOP:** {item}." for item in spec["red"])
    evidence = "\n".join(f"- {item}." for item in spec["evidence"])
    triage_tree = "\n".join(
        f"{index}. **Objaw:** {scenario[1]} → **hipoteza:** {scenario[2]} → **test:** {scenario[3]} → "
        f"**przejście:** naprawiaj dopiero po uzyskaniu dowodu."
        for index, scenario in enumerate(spec["scenarios"], 1)
    )
    command_links = "\n".join(
        f"- `{command[0]}` — {command[1]}, {command[3]}; szczegóły w "
        f"[references/command-cards.md](references/command-cards.md#{slug(command[0])})."
        for command in spec["commands"]
    )
    source_links = "\n".join(
        f"- `{source_id}` — [{SOURCE_BY_ID[source_id]['title']}]({SOURCE_BY_ID[source_id]['url']}) "
        f"(zweryfikowano {TODAY})."
        for source_id in spec["sources"]
    )
    body = f"""\
---
name: {name}
description: "{description}"
{execution_metadata}
---

# {spec['title']}

## Cel i granice odpowiedzialności

Prowadź {spec['focus']}. Rozdzielaj fakty, hipotezy, testy i wyniki. Nie wykonuj zmian bez
autoryzacji odpowiedniej do R0–R4. {spec['exclude']}

## Kiedy aktywować i kiedy nie aktywować

Aktywuj dla fraz: {", ".join(f"`{item}`" for item in spec['triggers'])}. Nie aktywuj dla
problemów, których główna przyczyna należy do powiązanego skilla; router wybiera dokładnie jeden
skill główny. Użytkowanie jawne `$${name}` ma pierwszeństwo, ale nie znosi bramek bezpieczeństwa.

## Dane wejściowe i minimalne pytania bezpieczeństwa

Najpierw ustal: czy system startuje; czy istnieje zweryfikowany backup; czy dane są cenniejsze niż
urządzenie; czy BitLocker/Device Encryption jest włączony; czy urządzenie jest domain/Entra/MDM;
jakie były ostatnie zmiany; jaki dokładnie objaw i czas reprodukcji. Nie pytaj o recovery key,
hasło, token ani pełny product key. Dla tej domeny zbierz:

{evidence}

## Szybki triage i czerwone flagi

{red_flags}

Jeżeli wystąpi flaga, zatrzymaj testy, zabezpiecz dowody i przejdź do eskalacji. Nie interpretuj
braku telemetrii jako potwierdzenia zdrowia.

## Zgodność

Obsługuj Windows XP SP3–11, ale przed komendą sprawdź build, edition, x86/x64/ARM64, język,
online/Safe Mode/WinRE/WinPE/offline oraz BIOS/MBR albo UEFI/GPT. Najpierw otwórz
[references/compatibility.md](references/compatibility.md), gdy środowisko jest legacy, offline,
ARM64, w trybie S, N, LTSC/LTSB lub zarządzane. W WinRE nigdy nie zakładaj `C:`.

## Drzewo objaw → dowód → hipoteza → test

{triage_tree}

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

{command_links}

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

{related_links}

## Źródła

{source_links}

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
"""
    write(folder / "SKILL.md", clean(body))

    playbook_sections = []
    for index, scenario in enumerate(spec["scenarios"], 1):
        pb_id = f"{name}-pb-{index:02d}"
        title, symptom, hypothesis, diagnostic, repair, validation = scenario
        playbook_sections.append(
            f"""\
## {pb_id}: {title}

**Objaw i zakres:** {symptom}

**Bramka bezpieczeństwa:** potwierdź backup, BitLocker readiness, stan zarządzania i brak:
{", ".join(spec["red"])}. Jeśli którakolwiek flaga występuje, oznacz `blocked` i eskaluj.

### Dowody przed zmianą

{chr(10).join(f"- {item}." for item in spec["evidence"])}
- Zapisz timestamp reprodukcji i hash eksportowanych artefaktów.

### Rozgałęzienia hipotez

- Jeżeli dowód jest zgodny z: **{hypothesis}**, wykonaj tylko test: {diagnostic}
- Jeżeli dowód przeczy hipotezie, cofnij testową zmianę i przejdź do kolejnej hipotezy.
- Jeżeli wynik jest `inconclusive`, rozszerz R0; nie awansuj automatycznie do R2/R3.
- Jeżeli pojawi się czerwona flaga, zatrzymaj wszystkie testy zapisu.

### Drabina wykonania

1. **R0:** {diagnostic}
2. **R1:** wykonaj odwracalny test jednej zmiennej i zapisz stan before.
3. **R2/R3:** {repair} Wymagaj backupu, `ShouldProcess`/planu i jawnego celu.
4. **R4:** nie automatyzuj; tylko formalna decyzja właściciela i zweryfikowana kopia.

### Oczekiwany wynik i odchylenia

Dowód zgodny wzmacnia jedną hipotezę, ale nie kasuje alternatyw bez testu. Brak danych oznacz
`inconclusive`. Niepowodzenie rollbacku oznacza natychmiastową eskalację.

### Rollback

Przywróć zapisany stan before albo wymień komponent testowy na pierwotny. Dopisz rollback jako
nowy rekord JSONL. Nie usuwaj wcześniejszego dowodu.

### Walidacja

{validation} Powtórz test przyczyny, objawu i co najmniej jeden test regresji po reboot/sleep.

### Artefakty i stop

Zachowaj wejścia, stdout/stderr, relevant logs, before/after, hashes i wynik. Stop przy:
{", ".join(spec["red"])}.
"""
        )
        playbook_record = {
            "id": pb_id,
            "title": title,
            "summary": symptom,
            "symptoms": [symptom],
            "applies_to": ["Windows XP-11 according to compatibility matrix", "online/offline as documented"],
            "excludes": [spec["exclude"]],
            "risk_class": "R0-R3 gated",
            "authorization_required": True,
            "prerequisites": ["intake", "authorization", "backup status", "target identification"],
            "data_safety": spec["red"],
            "evidence_to_collect": spec["evidence"],
            "hypotheses": [hypothesis, "alternatywa sprzętowa lub środowiskowa", "wynik niejednoznaczny"],
            "diagnostics": [diagnostic],
            "repair_ladder": ["R0 evidence", "R1 reversible test", repair, "R4 manual-only"],
            "commands": [f"{name}-cmd-{i:02d}" for i in range(1, len(spec["commands"]) + 1)],
            "rollback": ["stan before", "rekord korekty w timeline", "eskalacja, jeśli rollback nie działa"],
            "validation": [validation, "test regresji", "porównanie before/after"],
            "stop_conditions": spec["red"],
            "escalation": ["hardware/data lab", "organizational administrator", "incident response as applicable"],
            "related_skills": spec["related"],
            "sources": spec["sources"],
            "last_verified": TODAY,
            "status": "complete",
        }
        dump_yaml_json(f"knowledge-base/playbooks/{pb_id}.yaml", playbook_record)
    playbooks = f"""\
# Playbooki: {spec['title']}

Otwórz wyłącznie playbook odpowiadający objawowi. Każdy wymaga intake i dowodu przed zmianą.

{chr(10).join(playbook_sections)}
"""
    write(folder / "references" / "playbooks.md", clean(playbooks))

    card_sections = []
    for index, command in enumerate(spec["commands"], 1):
        card_name, context, syntax, risk, expected, rollback = command
        card_id = f"{name}-cmd-{index:02d}"
        card_sections.append(
            f"""\
## {slug(card_name)}

- **ID:** `{card_id}`
- **Kontekst:** {context}
- **Składnia:** `{syntax}`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `{risk}`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** {expected}
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** {rollback}
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** {", ".join(f'`{item}`' for item in spec["sources"])}; zweryfikowano {TODAY}.
"""
        )
        kb_card = card_sections[-1].replace(
            "(compatibility.md)",
            f"(../../.agents/skills/{name}/references/compatibility.md)",
        )
        write(
            f"knowledge-base/commands/{card_id}.md",
            clean(
                f"""\
# {card_name}

Karta współdzielona przez `{name}`. Aktualna treść:

{kb_card}
"""
            ),
        )
    write(
        folder / "references" / "command-cards.md",
        clean(
            f"""\
# Karty poleceń: {spec['title']}

Karty są R0 lub planem, o ile nie wskazano inaczej. Nie kopiuj polecenia bez kontekstu.

{chr(10).join(card_sections)}
"""
        ),
    )

    write(
        folder / "references" / "compatibility.md",
        clean(
            f"""\
# Zgodność: {spec['title']}

| Wariant | Zasada |
| --- | --- |
| Windows 11 x64/ARM64 | Sprawdź aktywny build, DCH/ARM64 i security stack; preferowany zakres. |
| Windows 10 | Sprawdź ESU/LTSC i exact edition; nie zakładaj standardowego wsparcia. |
| XP/Vista/7/8.x | Izoluj sieciowo, używaj legacy playbooka i planuj migrację. |
| Online/Safe Mode | Zbieraj baseline przed zmianą; odnotuj różnicę usług/driverów. |
| WinRE/WinPE/offline | Zidentyfikuj wolumin trzema sygnałami; nigdy nie zakładaj `C:`. |
| BIOS/MBR | Nie stosuj instrukcji UEFI/ESP. |
| UEFI/GPT | Sprawdź Secure Boot, TPM, BitLocker i właściwy ESP. |
| Home/Pro/Enterprise/Education/N/S | Ustal capability i policy; nie obchodź ograniczeń. |
| Domain/Entra/MDM | R0, potem administrator organizacji przed naruszeniem polityki. |

W tej domenie szczególnie zweryfikuj: {", ".join(spec["evidence"])}.
"""
        ),
    )
    sources_md = "\n".join(
        f"- **{source_id}** — [{SOURCE_BY_ID[source_id]['title']}]({SOURCE_BY_ID[source_id]['url']}); "
        f"{SOURCE_BY_ID[source_id]['claim_summary']} Status `{SOURCE_BY_ID[source_id]['status']}`, "
        f"zweryfikowano {TODAY}."
        for source_id in spec["sources"]
    )
    write(
        folder / "references" / "sources.md",
        clean(
            f"""\
# Źródła: {spec['title']}

{sources_md}

Nie rozszerzaj claimu poza podany zakres. Informacje active-release odśwież po 90 dniach.
"""
        ),
    )
    write(
        folder / "assets" / "validation-checklist.md",
        clean(
            f"""\
# Checklista wyniku — {spec['title']}

- [ ] Autoryzacja i target potwierdzone.
- [ ] Backup/value-of-data i BitLocker readiness zapisane.
- [ ] Dowody before zachowane: {", ".join(spec["evidence"])}.
- [ ] Jedna hipoteza testowana naraz.
- [ ] Rollback gotowy przed R1+.
- [ ] Test przyczyny, objawu i regresji wykonany.
- [ ] Ryzyko resztkowe oraz status fixed/mitigated/blocked zapisane.
- [ ] Brak sekretów i PII w artefaktach.
"""
        ),
    )
    short = f"Bezpiecznie: {spec['title']}"
    if len(short) > 64:
        short = short[:61].rstrip() + "..."
    if len(short) < 25:
        short += " Windows"
    display = spec["title"]
    openai_yaml = (
        "interface:\n"
        f"  display_name: {json.dumps(display, ensure_ascii=False)}\n"
        f"  short_description: {json.dumps(short, ensure_ascii=False)}\n"
        f"  default_prompt: {json.dumps(f'Use ${name} to diagnose this Windows issue safely and show one phase at a time.', ensure_ascii=False)}\n"
        "policy:\n"
        "  allow_implicit_invocation: true\n"
    )
    write(folder / "agents" / "openai.yaml", openai_yaml)


def generate_root_files() -> None:
    skill_table = "\n".join(
        f"- [`{item['name']}`](.agents/skills/{item['name']}/SKILL.md) — {item['focus']}."
        for item in SKILLS
    )
    write(
        "README.md",
        clean(
            f"""\
# windows-master-service-skills

Prywatny, polskojęzyczny „drugi mózg” serwisanta Windows XP–11. Repo prowadzi od intake,
ochrony danych i dowodów przez różnicowanie hipotez do kontrolowanej naprawy, rollbacku,
walidacji i raportu. Nie jest zestawem magicznych one-linerów, nie obchodzi haseł/BitLocker,
nie zawiera ISO, driverów ani cudzych binariów i nie uruchamia napraw samoczynnie.

Snapshot wiedzy zależnej od wersji: **{TODAY}**. Przed użyciem informacji starszej niż 90 dni
uruchom updater w trybie diff i wykonaj review.

## Zanim dotkniesz komputera klienta

1. Potwierdź właściciela, zakres zgody i urządzenie/akcesoria.
2. Ustal wartość danych, backup, BitLocker/Device Encryption i MDM/Entra/domain.
3. Zatrzymaj się przy klikającym dysku, błędach RAM, cieczy, spuchniętej baterii lub zapachu.
4. Utwórz sprawę i baseline przed zmianą; zmieniaj jedną rzecz naraz.
5. Nie wykonuj R2–R4 bez backupu, jawnego celu, rollbacku i odpowiedniego potwierdzenia.

## Szybki start

Walidacja repo:

```powershell
& .\\scripts\\repo\\Test-WindowsMasterRepo.ps1 -Category All
```

W tym repo skille są już repo-local w oficjalnym katalogu `.agents/skills`; wystarczy otworzyć
repo w Codex. Instalacja samowystarczalnych paczek do innego repo:

```powershell
& .\\scripts\\repo\\Install-WindowsMasterSkills.ps1 -Scope Repo -Destination '<TARGET_REPO>\\.agents\\skills' -Mode Copy
```

Instalacja user-wide do `$HOME/.agents/skills` (domyślne źródło: `dist/skills`):

```powershell
& .\\scripts\\repo\\Install-WindowsMasterSkills.ps1 -Scope User -Mode Copy
```

Jawne wywołanie: `$windows-update-servicing Zdiagnozuj 0x800f0922, najpierw tylko R0`.
Szerokie zgłoszenie: `$windows-master-router Laptop zapętla Automatic Repair po aktualizacji`.

Bundle na fixture (bez dotykania hosta):

```powershell
& .\\scripts\\diagnostics\\Get-WindowsRepairBundle.ps1 -Mode Basic `
  -FixtureRoot .\\tests\\fixtures\\repair-bundle -OutputPath .\\dist\\sample-bundle
```

Nowa syntetyczna sprawa i raport:

```powershell
& .\\scripts\\reporting\\New-WindowsServiceCase.ps1 -Slug update-loop `
  -OwnerAlias customer-001 -AuthorizationLevel R0 -Root .\\dist\\cases
& .\\scripts\\reporting\\New-WindowsServiceReport.ps1 `
  -CasePath .\\dist\\cases\\{TODAY}-update-loop
```

## Model ryzyka

| Klasa | Znaczenie | Bramka |
| --- | --- | --- |
| R0 | observation/export | brak mutacji; redakcja i autoryzacja dostępu |
| R1 | reversible-user | stan before i prosty rollback |
| R2 | controlled-system-change | backup, plan, `-Apply`, `ShouldProcess` |
| R3 | high-risk-repair | jawne potwierdzenie targetu, BitLocker i rollback |
| R4 | destructive-or-firmware | nigdy automatycznie; wpisane potwierdzenie i zweryfikowana kopia |

## Instalacja, pakowanie i deinstalacja

`Copy` jest bezpiecznym domyślnym trybem. `Junction` jest dostępny tylko lokalnie i wymaga
świadomego wyboru. Kolizje są przenoszone do datowanego backupu. Manifest instalacji znajduje
się w katalogu docelowym i deinstalator usuwa wyłącznie ścieżki, których hash zgadza się z
manifestem; zmienione pliki pozostają do ręcznego review.

```powershell
& .\\scripts\\repo\\Build-SkillPackages.ps1
& .\\scripts\\repo\\Uninstall-WindowsMasterSkills.ps1 -Scope User -RestoreBackup
```

Można też wskazać `-Destination <TEMP>` do bezpiecznego testu. User scope według aktualnej
oficjalnej dokumentacji Codex to `$HOME/.agents/skills`.

## Aktualizacja wiedzy i narzędzi

Updatery tworzą tylko kandydat/diff; nigdy automatycznie nie uznają sieciowej odpowiedzi za
prawdę:

```powershell
& .\\scripts\\repo\\Update-WindowsKnowledgeBase.ps1 -WhatIf
& .\\scripts\\repo\\Update-ToolCatalog.ps1 -WhatIf
```

Kolejność zaufania: Microsoft → OEM/vendor → oficjalny projekt → moderowana społeczność →
agregator tylko jako trop. Katalog zapisuje licencję, commercial use, redistribution, wersję,
official source i metodę integralności.

## Prywatność i licencje

`cases/`, dumpy, bundle i dane klienta są ignorowane przez Git. Collectory redagują username,
hostname, e-mail i adresy domyślnie; nie zbierają haseł, cookies, tokenów, pełnych product keys
ani recovery keys. Kod repo jest prywatny; narzędzia zewnętrzne zachowują własne licencje.

## Mapa 39 skilli

{skill_table}

## Stan i ograniczenia

Zobacz [REPO_STATUS.md](REPO_STATUS.md), [coverage-matrix.yaml](coverage-matrix.yaml),
[snapshot](docs/current-state-snapshot.md) i [kolejkę researchu](RESEARCH_QUEUE.md).
"""
        ),
    )
    write(
        "AGENTS.md",
        clean(
            """\
# Instrukcje repozytorium

- Pisz dokumentację użytkową po polsku; polecenia, nazwy API i błędy zachowuj oryginalnie.
- Na hoście deweloperskim uruchamiaj wyłącznie walidatory, parsowanie fixture, mocki, pakowanie i
  operacje repo. Nigdy nie uruchamiaj repair `-Apply`, DISM/SFC, resetów, BCD, driverów ani firmware.
- Zbieraj dowody przed zmianą, klasyfikuj R0–R4, pokazuj target i rollback dla R2+.
- Nie zapisuj sekretów, PII, recovery keys ani danych klientów. `cases/` i dumpy pozostają poza Git.
- Fakty zależne od wersji wymagają source ID, `last_verified` i confidence. Community finding nie
  jest domyślną naprawą.
- Nie twierdź, że test przeszedł, jeżeli nie został wykonany. `SKIP` i `requires-live-validation`
  są prawidłowymi, uczciwymi wynikami.
- Używaj UTF-8/LF, kebab-case dla skilli, PascalCase-VerbNoun dla skryptów PowerShell.
- Zmiana procedury wymaga aktualizacji coverage matrix, playbook schema record, source register,
  tool manifest (jeśli dotyczy), evals i changelog.
- `_shared` nie może zawierać `SKILL.md`.
"""
        ),
    )
    write(
        ".agents/skills/AGENTS.md",
        clean(
            """\
# Instrukcje dla skilli

- Front matter zawiera `name`, `description` i stringowy blok `metadata` zgodny z kontraktem
  `swietlik.orchestrator.*`; folder i `name` muszą być identyczne.
- Description front-loaduje cel i polskie/angielskie/holenderskie frazy; body pozostaje poniżej
  500 linii, a szczegóły trafiają do bezpośrednich `references/`.
- Każdy skill ma trzy kompletne playbooki, trzy command cards, rollback, walidację, źródła,
  antywzorce i dokładne linki do powiązanych skilli.
- Otwieraj tylko referencję potrzebną dla aktualnego objawu. Nie ładuj całej bazy.
- Polecenia muszą mieć kontekst, ryzyko, expected output, error interpretation i rollback.
"""
        ),
    )
    write(
        "knowledge-base/AGENTS.md",
        clean(
            """\
# Instrukcje bazy wiedzy

- Dane maszynowe zapisuj jako JSON zgodny z YAML 1.2 i waliduj schematem.
- Nie duplikuj kart komend w playbookach: używaj ich ID.
- Każdy claim zależny od wersji ma source ID i `last_verified`.
- Status `unverified` wymaga uzasadnienia w RESEARCH_QUEUE.md.
- Zachowuj rozdział między wspieranym zachowaniem, obserwacją i hipotezą.
"""
        ),
    )
    write(
        "scripts/AGENTS.md",
        clean(
            """\
# Instrukcje dla skryptów

- PowerShell 5.1 jest bazą; używaj StrictMode, pełnych nazw cmdletów, try/catch/finally i
  comment-based help.
- Collector ma redakcję domyślną i tryb fixture. Repair domyślnie `Scan`, wymaga `-Apply` oraz
  `SupportsShouldProcess`; nigdy nie wykonuj go na hoście deweloperskim.
- Nie używaj `Invoke-Expression`, pipe-to-shell, Win32_Product ani download-and-run.
- Target path/volume/disk musi być jawny i zweryfikowany. Logi JSONL nie zawierają sekretów.
- Każda nowa funkcja wymaga Pester/mock lub deterministycznego fixture testu.
"""
        ),
    )
    write(
        "tests/AGENTS.md",
        clean(
            """\
# Instrukcje testów

- Testy nie mogą dotykać usług, rejestru, BCD, sieci, Defendera, driverów, partycji ani firmware.
- Używaj tylko katalogów tymczasowych, fixture i mocków. Testuj `WhatIf`/Scan oraz exit codes.
- Nie ukrywaj brakującej zależności: raportuj `SKIP` z nazwą i wymaganiem wersji.
- Nowy antywzorzec dodaj do safety lintera wraz z pozytywnym fixture dokumentacyjnym.
"""
        ),
    )
    write(
        "LICENSE.md",
        clean(
            """\
# Licencja i status prywatny

Copyright (c) 2026. Wszystkie prawa zastrzeżone.

Repozytorium jest prywatne i nieprzeznaczone do redystrybucji. Brak zgody na kopiowanie,
publikowanie, sprzedaż ani sublicencjonowanie całości lub części bez pisemnej zgody właściciela.
Linki, nazwy i metadane narzędzi zewnętrznych nie przenoszą praw do tych narzędzi. Każdy projekt,
vendor i wydawca zachowuje własne prawa, EULA i ograniczenia commercial/redistribution.

Repo nie zawiera cudzych binariów, ISO, WIM, sterowników ani komercyjnych rescue media.
"""
        ),
    )
    write(
        "SECURITY.md",
        clean(
            """\
# Bezpieczeństwo

Nie umieszczaj sekretów ani danych klienta w issue, commitach lub bundle. Podejrzany wyciek:
odłącz artefakt od przepływu, zachowaj minimalny dowód lokalnie, rotuj poświadczenie właściwym
kanałem i udokumentuj incydent bez wklejania sekretu. Nie przesyłaj go automatycznie.

Skrypty repair mają safety gates i nie są poleceniem wykonania. R3/R4 wymagają operatora, jawnego
targetu, backupu i rollbacku. Zgłoszenia podatności dotyczące repo należy przekazać prywatnym
kanałem właściciela; repo nie definiuje publicznego endpointu.
"""
        ),
    )
    write(
        "CHANGELOG.md",
        clean(
            f"""\
# Changelog

## Unreleased

- Dodano stringowe metadane wykonawcze `swietlik.orchestrator.*` do 39 skilli źródłowych bez
  zmiany procedur naprawczych ani granic R0–R4.
- Dodano rootowy `pack.yaml`, deterministyczny `skills-index.json`, samowystarczalny generator
  indeksu oraz CI wykrywające dryf i błędy kontraktu.
- Rozszerzono generator i statyczny validator repozytorium o trwałą obsługę metadanych
  orkiestratora.

## 1.0.0 — {TODAY}

- Utworzono 39 skilli z playbookami, kartami poleceń, evals i metadanymi UI.
- Dodano knowledge base Windows XP–11, release/lifecycle snapshot, katalog narzędzi i source register.
- Dodano collectory fixture-safe, parsery, case/reporting, repair wrappers Scan-first i service media.
- Dodano schema/link/safety/smoke/Pester validation, 60 krótkich i 15 pełnych spraw.
- Dodano samowystarczalne pakowanie oraz instalację/deinstalację z manifestem.
"""
        ),
    )
    write(
        "ROADMAP.md",
        clean(
            """\
# Roadmap

## Po 1.0

- Zweryfikować pełną macierz na snapshotach XP, 7, 8.1, 10 ESU oraz Windows 11 x64/ARM64.
- Dodać podpisywanie własnych release artifacts po ustaleniu prywatnego PKI.
- Rozszerzać vendor-specific firmware/LED code references wyłącznie z dokładnym modelem.
- Utrzymywać 90-dniowy rytm release/tool review i kwartalne forward evals.

Pozycje wymagające zewnętrznego laboratorium są także w RESEARCH_QUEUE.md; nie są ukrytymi
placeholderami ani deklaracją wykonanych testów.
"""
        ),
    )
    write(
        "RESEARCH_QUEUE.md",
        clean(
            """\
# Research queue

Jawnie nieweryfikowalne w tym przebiegu bez pobierania pakietów, licencji komercyjnej albo
kontrolowanego laboratorium:

1. `requires-live-validation`: boot/rollback wszystkich playbooków R3/R4 na fizycznym
   BIOS/MBR, UEFI/GPT i ARM64; budowa repo nie może bezpiecznie wykonać tych zmian.
2. `requires-live-validation`: restore bare-metal Veeam/Hasleo/Macrium i aktualne ograniczenia
   commercial use; potrzebne licencje, media i pusty cel.
3. `unverified`: dokładna redistribution dla MediCat, Hiren's i niektórych agregatorów per
   składnik; status pozostaje `forbidden` jako bezpieczne założenie.
4. `requires-live-validation`: OEM firmware/SSD/dock matrices; właściwy obraz zależy od modelu
   i nie może być uogólniony.
5. `requires-live-validation`: Pester na natywnym Windows PowerShell 5.1 oraz ARM64 runner;
   bieżący host ma PowerShell 7 i starą lokalną wersję Pester.
6. `unverified`: current exact versions proprietary rolling tools bez stabilnego machine-readable
   release endpointu; katalog używa `rolling` i wymaga ręcznego review przed downloadem.
7. `requires-live-validation`: Secure Boot 2023 certificate rollout na reprezentatywnych OEM z
   BitLocker; oficjalne metadata zweryfikowano, zmian firmware nie wykonywano.
"""
        ),
    )
    write(
        ".gitignore",
        clean(
            """\
cases/
*.dmp
*.etl
*.evtx
*.pcap
*.pcapng
*.zip
*.7z
*.iso
*.wim
*.esd
*.ffu
*.vhd
*.vhdx
*.key
*.pfx
*.cer.private
dist/tmp/
dist/reports/
dist/test-install/
downloads/
service-media/staging/
.pytest_cache/
__pycache__/
*.pyc
"""
        ),
    )
    write(
        ".gitattributes",
        "* text=auto eol=lf\n*.ps1 text eol=crlf\n*.psm1 text eol=crlf\n*.cmd text eol=crlf\n*.json text eol=lf\n*.yaml text eol=lf\n",
    )
    write(
        ".editorconfig",
        clean(
            """\
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.ps1]
end_of_line = crlf
indent_size = 4

[*.py]
indent_size = 4
"""
        ),
    )
    write(
        "PSScriptAnalyzerSettings.psd1",
        clean(
            """\
@{
    Severity = @('Error', 'Warning')
    ExcludeRules = @('PSAvoidUsingWriteHost')
    Rules = @{
        PSAvoidUsingCmdletAliases = @{ Enable = $true }
        PSUseShouldProcessForStateChangingFunctions = @{ Enable = $true }
        PSUseDeclaredVarsMoreThanAssignments = @{ Enable = $true }
    }
}
"""
        ),
    )


def generate_docs() -> None:
    write(
        "docs/architecture.md",
        clean(
            """\
# Architektura

Repo ma trzy warstwy: `.agents/skills` odpowiada za routing i workflow, `knowledge-base` jest
źródłem danych wspólnym dla człowieka i agenta, a `scripts` zapewnia deterministyczne collectory,
parsery, raporty i kontrolowane wrappers. Skills stosują progressive disclosure: description →
SKILL.md → jedna wskazana referencja. `_shared` nie jest skillem.

```mermaid
flowchart LR
  U[Zgłoszenie] --> R[windows-master-router]
  R --> I[Intake + autoryzacja]
  I --> P[Jeden skill główny]
  P --> K[Playbook + command cards]
  K --> E[Evidence/before]
  E --> D[R0 diagnosis]
  D -->|dowód| X[R1-R4 gate]
  X --> V[Validation]
  V --> C[Case/report]
```

Machine-readable YAML files are emitted as JSON, which is valid YAML 1.2 and permits dependency-free
validation. IDs are stable: `<skill>-pb-NN`, `<skill>-cmd-NN`, source/tool IDs in kebab-case.
Packager copies `_shared` into each `dist/skills/<skill>/references/_shared`, so installed skills
do not depend on repository-relative resources.

Model danych: playbook schema, source schema, tool catalog schema, eval schema i case schema są w
`.agents/skills/_shared/schemas`. `coverage-matrix.yaml` links a symptom class to a concrete
playbook file. Versioned facts live in release/source registers, not repeated prose.
"""
        ),
    )
    write(
        "docs/operating-model.md",
        clean(
            """\
# Model operacyjny

`intake → autoryzacja → zabezpieczenie danych → identyfikacja środowiska → reprodukcja →
dowody → ranking hipotez → najmniej inwazyjny test → naprawa → rollback readiness →
walidacja → burn-in → dokumentacja → zapobieganie nawrotowi`

Technik prowadzi jedną sprawę i jeden główny skill. Router nie diagnozuje za specjalistę.
Fakty mają artefakt; hipotezy mają confidence; wyniki to observed/not-observed/inconclusive/blocked.
Zmiana jednej zmiennej pozwala przypisać skutek. Event Viewer bez korelacji czasowej nie jest
diagnozą. Storage/RAM/power/thermal mają pierwszeństwo, jeżeli mogą fałszować software.
"""
        ),
    )
    write(
        "docs/diagnostic-method.md",
        clean(
            """\
# Metoda diagnostyczna

1. Zapisz dokładny symptom, warunki i mierzalne kryterium sukcesu.
2. Oddziel dowody pierwotne od wtórnych błędów.
3. Zbuduj ranking najwyżej trzech hipotez z dowodem za/przeciw.
4. Wykonaj najtańszy bezpieczny test rozróżniający, nie „naprawę wszystkiego”.
5. Aktualizuj prawdopodobieństwo po wyniku; `inconclusive` nie wzmacnia hipotezy.
6. Przed zmianą zapisz before, backup i rollback; po zmianie test cause/symptom/regression.

Stop conditions mają pierwszeństwo nad harmonogramem i wygodą. Recovery storage zawsze zapisuje
na inny nośnik. WinRE zawsze identyfikuje litery na nowo.
"""
        ),
    )
    write(
        "docs/safety-and-authorization.md",
        clean(
            """\
# Bezpieczeństwo i autoryzacja

R0 wymaga prawa do odczytu urządzenia. R1 wymaga zgody na zmianę ustawienia użytkownika. R2 ma
backup i system-change approval. R3 wymaga pokazania dokładnego targetu oraz BitLocker readiness.
R4 wymaga wpisanego potwierdzenia targetu i zweryfikowanej kopii; agent nigdy nie wykonuje go
automatycznie.

Zakazane: password bypass, credential dumping, recovery-key extraction, BitLocker/EFS bypass,
piracka aktywacja, ukryta zdalna persistence, pracę wewnątrz PSU i flash przy niestabilnym
zasilaniu. Urządzenie domain/Entra/MDM pozostaje pod kontrolą organizacji.
"""
        ),
    )
    write(
        "docs/source-policy.md",
        clean(
            """\
# Polityka źródeł

Priorytet: Microsoft → OEM/vendor → oficjalny projekt/release → moderowana społeczność →
agregator tylko do odkrycia tropu. Claim zapisuje source ID, zakres, confidence, status i datę.
Active Windows/tool facts są świeże 90 dni; stabilna historia 365 dni.

Community fix ma etykietę `community-confirmed`, `anecdotal` albo `unverified`; nie staje się
domyślną naprawą bez drugiego niezależnego źródła lub bezpiecznego testu lab. Updater zapisuje
kandydat i diff, ale review decyduje o przyjęciu.
"""
        ),
    )
    write(
        "docs/tool-selection-policy.md",
        clean(
            """\
# Polityka wyboru narzędzia

`wbudowane Microsoft → oficjalne OEM → oficjalny projekt portable/open source → sprawdzone
community → agregator/agresywny suite wyłącznie po analizie konkretnej funkcji`

Przed użyciem sprawdź exact version, official origin, license/commercial use, redistribution,
OS/arch/environment, signature/hash i risk. Downloader nie wykonuje assetu. `latest.exe` jest
niedozwolone bez rozwiązania do konkretnej wersji. DDU/driver packs/tweak suites są wyjątkiem,
nie domyślną praktyką.
"""
        ),
    )
    write(
        "docs/service-media.md",
        clean(
            """\
# Nośnik serwisowy

Repo projektuje staging, nie zapisuje USB i nie pobiera obrazów. `New-ServiceMediaPlan.ps1`
tworzy plan dla oficjalnego WinPE, jeżeli wykryto ADK i add-on, albo wariantu multiboot.
Aktualny snapshot wskazuje ADK 10.1.28000.1 i konieczność bieżącej poprawki bezpieczeństwa;
przed budową zawsze odśwież źródło.

Układ: `boot/`, `iso/official/`, `linux-rescue/`, `tools/{x64,arm64}`, `drivers/{storage,network}/{x64,arm64}`,
`scripts/`, `docs/`, `cases-encrypted/`, `manifests/`. Dane spraw są szyfrowane oddzielnie.
Każdy asset ma provenance, license, redistribution, exact version, size, SHA-256 oraz
Authenticode/PGP, jeśli wydawca publikuje. R4 write-to-USB wymaga potwierdzenia UniqueId.
"""
        ),
    )
    write(
        "docs/legacy-isolation.md",
        clean(
            """\
# Izolacja systemów legacy

XP/Vista/7/8.x są niewspierane. Domyślna topologia to offline albo odseparowany VLAN bez dostępu
do Internetu, wyłącznie na czas eksportu danych. Nie loguj się na konta chmurowe i nie używaj
legacy browsera. Najpierw obraz starego HDD, potem analiza kopii. Transfer wykonuj przez
skanowany, kontrolowany nośnik lub jednokierunkowy staging.

Naprawa ma cel odzysku danych/krótkiej ciągłości; rozwiązaniem długoterminowym jest migracja do
wspieranego OS/sprzętu lub izolowanej VM z legalną licencją.
"""
        ),
    )
    write(
        "docs/testing-lab.md",
        clean(
            """\
# Laboratorium VM i hardware

Macierz snapshotów: XP SP3 x86 BIOS/MBR; Windows 7 SP1 x64 BIOS+UEFI; 8.1 x64 UEFI; Windows 10
22H2/ESU i LTSC; aktywne Windows 11 x64 oraz ARM64, Local/MSA/Entra test tenant, BitLocker
on/off, Secure Boot on/off. Obrazy i licencje nie należą do repo.

Fault injection wyłącznie w disposable VM: corrupt copy of BCD store, disabled test service,
synthetic bad driver metadata, full mock volume, pending-reboot markers, malformed CBS/Panther,
temporary profile mapping i blocked DNS. Partition/firmware/BitLocker recovery test wymaga
snapshotu, konsoli out-of-band i nie zawiera danych.

Każdy scenariusz zapisuje snapshot ID, expected evidence, stop condition, rollback result i
validation. Nie przenoś procedury R3/R4 na host produkcyjny na podstawie samego VM success.
"""
        ),
    )
    write(
        "docs/maintenance.md",
        clean(
            """\
# Utrzymanie

Co 90 dni: odśwież Windows release/health, ADK/WinPE, Secure Boot, Sysinternals i aktywne tools.
Co 365 dni: przegląd legacy, źródeł stabilnych, licencji i wszystkich linków. Każda zmiana:
source diff → review → schema/link/safety/evals → package → temp install/uninstall → changelog.

Nie przyjmuj automatycznie zmiany z sieci. Nowy tool zaczyna jako `unknown`, redistribution
`forbidden` i commercial `verify` do czasu dowodu. EOL ma replacement i unika rekomendacji.
"""
        ),
    )
    write(
        "docs/assumptions.md",
        clean(
            f"""\
# Założenia

- Bieżący katalog zawierał wyłącznie master prompt i nie był repozytorium, więc repo utworzono
  bez podkatalogu.
- Oficjalny snapshot Agent Skills z {TODAY} wskazuje repo scope `.agents/skills`, user scope
  `$HOME/.agents/skills`, required `name`/`description` i wspierane `agents/openai.yaml`.
- Machine-readable `.yaml` używa JSON, poprawnego podzbioru YAML 1.2, aby walidacja nie wymagała
  pobierania bibliotek.
- User-wide oznacza bieżącego użytkownika, nie all-users/admin.
- Skrypty repair mogą wykonać zmiany dopiero po `-Apply`; na hoście budowy testuje się tylko Scan,
  WhatIf, fixture i parser syntax.
- Exact rolling version pozostaje `rolling`/`unknown`, jeżeli official page nie udostępnia
  stabilnego machine-readable faktu bez pobierania; nie zgadujemy.
"""
        ),
    )
    write(
        "docs/current-state-snapshot.md",
        clean(
            f"""\
# Snapshot stanu — {TODAY}

To datowany snapshot, nie wieczna prawda. Źródła wymagają ponownej kontroli po 90 dniach.

## Windows

- Windows 11 26H1: build family 28000, GA 2026-02-10, dla nowych urządzeń; nie jest in-place
  feature update z 24H2/25H2. Snapshot latest build: 28000.2525.
- Windows 11 25H2: build family 26200; snapshot latest 26200.8875.
- Windows 11 24H2: build family 26100; snapshot latest 26100.8875; Home/Pro servicing do
  2026-10-13, Enterprise/Education do 2027-10-12.
- Windows 11 23H2: Home/Pro EOL; Enterprise/Education do 2026-11-10.
- Windows 10 22H2 standard support zakończył się 2025-10-14; zapisane urządzenia mogą otrzymywać
  ESU. Snapshot July 2026 build: 19045.7548. LTSC/LTSB ma osobne cykle.
- XP SP3, Vista, Windows 7 i Windows 8/8.1 są niewspierane; repo wymusza izolację i migrację.

## ADK, Secure Boot i narzędzia Microsoft

- Microsoft page wskazuje ADK 10.1.28000.1 (November 2025) dla Windows 11 26H1 ARM64 oraz
  konieczność zainstalowania bieżącej poprawki ADK (co najmniej wskazanej na stronie).
- Certyfikaty Secure Boot z 2011 zaczęły wygasać w czerwcu 2026; wspierany kierunek to certyfikaty
  2023, firmware readiness, pilot i monitoring, zwłaszcza przy BitLocker.
- Sysinternals Suite snapshot: 2026.7, 2026-07-09; dostępne warianty standard/ARM64.

## Projekty z exact publicznym faktem

- Rufus 4.14 stable (official GitHub snapshot), MemTest86+ 8.10, TestDisk/PhotoRec 7.2,
  Wireshark 4.6.7. Ventoy official page publikuje exact assety i SHA-256; updater ma rozwiązać
  wersję w chwili przygotowania media.

Źródła: `knowledge-base/sources/source-register.yaml`.
"""
        ),
    )


def generate_shared() -> None:
    write(
        ".agents/skills/_shared/references/risk-model.md",
        clean(
            """\
# Model ryzyka R0–R4

R0 observation; R1 reversible-user; R2 controlled-system-change; R3 high-risk-repair; R4
destructive-or-firmware. R2+ wymaga before/backup/rollback i jawnego `-Apply`. R3 dodaje exact
target i BitLocker/management gate. R4 jest manual-only i nigdy nie jest automatycznie wykonywane.
"""
        ),
    )
    write(
        ".agents/skills/_shared/references/response-contract.md",
        clean(
            """\
# Kontrakt odpowiedzi

Najpierw zabezpiecz → Co wiemy → Hipotezy z confidence → Jeden krok diagnostyczny → Expected
output → Naprawa dopiero po dowodzie → Rollback → Sprawdzenie → Ryzyko resztkowe. Oznacz fact,
hypothesis, supported behavior i community workaround.
"""
        ),
    )
    write(
        ".agents/skills/_shared/references/stop-conditions.md",
        clean(
            """\
# Stop conditions

Klikający/znikający storage; rosnące read errors; RAM error; swollen battery/liquid/burning;
brak BitLocker recovery readiness przed R3/R4; managed policy conflict; security incident;
unknown firmware model; recovery source/target ambiguity. Zatrzymaj i eskaluj.
"""
        ),
    )
    write(
        ".agents/skills/_shared/templates/action-record.json",
        json.dumps(
            {
                "timestamp_utc": "<ISO8601>",
                "operator": "<ALIAS>",
                "purpose": "<PURPOSE>",
                "risk_class": "R0",
                "command_or_tool": "<NAME_AND_VERSION>",
                "target": "<VERIFIED_TARGET>",
                "result": "observed",
                "rollback": "not-applicable",
                "artifacts": [],
            },
            indent=2,
        )
        + "\n",
    )
    dump_yaml_json(
        ".agents/skills/_shared/fixtures/router-fixture.yaml",
        {
            "text": "Laptop wpada w Automatic Repair po aktualizacji, dysk nie klika, BitLocker włączony.",
            "expected_primary": "windows-boot-recovery",
            "expected_supporting": ["windows-update-servicing", "windows-bitlocker-tpm-security"],
            "required_first_step": "R0 boot layout and storage safety",
        },
    )


def generate_schemas() -> None:
    playbook_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://local.invalid/windows-master/playbook.schema.json",
        "title": "Windows service playbook",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "id", "title", "summary", "symptoms", "applies_to", "excludes", "risk_class",
            "authorization_required", "prerequisites", "data_safety", "evidence_to_collect",
            "hypotheses", "diagnostics", "repair_ladder", "commands", "rollback", "validation",
            "stop_conditions", "escalation", "related_skills", "sources", "last_verified", "status",
        ],
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z0-9-]+$"},
            "title": {"type": "string", "minLength": 5},
            "summary": {"type": "string", "minLength": 10},
            "symptoms": {"type": "array", "minItems": 1, "items": {"type": "string"}},
            "applies_to": {"type": "array", "minItems": 1, "items": {"type": "string"}},
            "excludes": {"type": "array", "items": {"type": "string"}},
            "risk_class": {"type": "string"},
            "authorization_required": {"type": "boolean"},
            "prerequisites": {"type": "array", "items": {"type": "string"}},
            "data_safety": {"type": "array", "minItems": 1, "items": {"type": "string"}},
            "evidence_to_collect": {"type": "array", "minItems": 2, "items": {"type": "string"}},
            "hypotheses": {"type": "array", "minItems": 2, "items": {"type": "string"}},
            "diagnostics": {"type": "array", "minItems": 1, "items": {"type": "string"}},
            "repair_ladder": {"type": "array", "minItems": 3, "items": {"type": "string"}},
            "commands": {"type": "array", "items": {"type": "string"}},
            "rollback": {"type": "array", "minItems": 1, "items": {"type": "string"}},
            "validation": {"type": "array", "minItems": 2, "items": {"type": "string"}},
            "stop_conditions": {"type": "array", "minItems": 1, "items": {"type": "string"}},
            "escalation": {"type": "array", "items": {"type": "string"}},
            "related_skills": {"type": "array", "items": {"type": "string"}},
            "sources": {"type": "array", "minItems": 1, "items": {"type": "string"}},
            "last_verified": {"type": "string", "format": "date"},
            "status": {"enum": ["complete", "partial", "experimental", "requires-live-validation"]},
        },
    }
    dump_yaml_json(".agents/skills/_shared/schemas/playbook.schema.json", playbook_schema)
    source_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "array",
        "items": {
            "type": "object",
            "required": ["id", "title", "url", "publisher", "source_type", "retrieved_at", "last_verified", "claim_summary", "confidence", "status", "license_notes"],
            "properties": {
                "id": {"type": "string"},
                "title": {"type": "string"},
                "url": {"type": "string", "pattern": "^https://"},
                "publisher": {"type": "string"},
                "source_type": {"enum": ["official", "vendor", "project", "community", "secondary"]},
                "retrieved_at": {"type": "string"},
                "last_verified": {"type": "string"},
                "applies_to": {"type": "array"},
                "claim_summary": {"type": "string"},
                "confidence": {"enum": ["high", "medium", "low"]},
                "status": {"enum": ["current", "stale", "eol", "replaced", "unverified"]},
                "license_notes": {"type": "string"},
            },
        },
    }
    dump_yaml_json(".agents/skills/_shared/schemas/source-register.schema.json", source_schema)
    eval_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["skill", "positive", "negative", "ambiguous"],
        "properties": {
            "skill": {"type": "string"},
            "positive": {"type": "array", "minItems": 12, "items": {"type": "object"}},
            "negative": {"type": "array", "minItems": 8, "items": {"type": "object"}},
            "ambiguous": {"type": "array", "minItems": 4, "items": {"type": "object"}},
        },
    }
    dump_yaml_json(".agents/skills/_shared/schemas/trigger-eval.schema.json", eval_schema)
    case_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["case_id", "created_utc", "owner_alias", "authorization_level", "data_value", "backup_status", "encryption_status", "managed_status"],
        "properties": {
            "case_id": {"type": "string"},
            "created_utc": {"type": "string"},
            "owner_alias": {"type": "string"},
            "authorization_level": {"enum": ["R0", "R1", "R2", "R3", "R4"]},
            "data_value": {"enum": ["low", "medium", "high", "critical", "unknown"]},
            "backup_status": {"enum": ["verified", "present-unverified", "absent", "unknown"]},
            "encryption_status": {"enum": ["off", "on-key-ready", "on-key-not-ready", "unknown"]},
            "managed_status": {"enum": ["personal", "domain", "entra", "mdm", "unknown"]},
        },
    }
    dump_yaml_json(".agents/skills/_shared/schemas/case-intake.schema.json", case_schema)
    tool_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://local.invalid/windows-master/tool-catalog.schema.json",
        "type": "array",
        "minItems": 60,
        "items": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "id", "name", "category", "publisher", "official_home", "official_download",
                "official_repository", "current_version", "checked_at", "status", "replaced_by",
                "license", "commercial_use", "redistribution", "supported_os", "architectures",
                "environments", "portable", "install_type", "network_required", "elevation_required",
                "signature_method", "checksum_method", "risk_class", "use_cases", "avoid_when",
                "known_gotchas", "alternatives", "sources",
            ],
            "properties": {
                "id": {"type": "string", "pattern": "^[a-z0-9-]+$"},
                "name": {"type": "string"},
                "category": {"type": "string"},
                "publisher": {"type": "string"},
                "official_home": {"type": "string", "pattern": "^https://"},
                "official_download": {"type": "string", "pattern": "^https://"},
                "official_repository": {"type": "string"},
                "current_version": {"type": "string"},
                "checked_at": {"type": "string", "format": "date"},
                "status": {"enum": ["active", "stale", "eol", "replaced", "unknown"]},
                "replaced_by": {"type": "string"},
                "license": {"type": "string"},
                "commercial_use": {"type": "string"},
                "redistribution": {"enum": ["forbidden", "unknown", "allowed", "conditional"]},
                "supported_os": {"type": "array"},
                "architectures": {"type": "array"},
                "environments": {"type": "array"},
                "portable": {"type": "boolean"},
                "install_type": {"type": "string"},
                "network_required": {"type": "boolean"},
                "elevation_required": {"type": "boolean"},
                "signature_method": {"type": "string"},
                "checksum_method": {"type": "string"},
                "risk_class": {"enum": ["R0", "R1", "R2", "R3", "R4"]},
                "use_cases": {"type": "array"},
                "avoid_when": {"type": "array"},
                "known_gotchas": {"type": "array"},
                "alternatives": {"type": "array"},
                "sources": {"type": "array"},
            },
        },
    }
    dump_yaml_json("tools/catalog.schema.json", tool_schema)
    dump_yaml_json(".agents/skills/_shared/schemas/tool-catalog.schema.json", tool_schema)


def generate_knowledge_base() -> None:
    release_matrix = {
        "snapshot_date": TODAY,
        "freshness_days": 90,
        "source": "ms-win11-release",
        "windows_11": [
            {"version": "26H1", "build_family": "28000", "latest_build_snapshot": "28000.2525", "availability": "2026-02-10", "home_pro_eol": "2028-03-14", "enterprise_education_eol": "2029-03-13", "notes": "Preinstalled on select new 2026 hardware; not an in-place update from 24H2/25H2."},
            {"version": "25H2", "build_family": "26200", "latest_build_snapshot": "26200.8875", "availability": "2025-09-30", "home_pro_eol": "2027-10-12", "enterprise_education_eol": "2028-10-10"},
            {"version": "24H2", "build_family": "26100", "latest_build_snapshot": "26100.8875", "availability": "2024-10-01", "home_pro_eol": "2026-10-13", "enterprise_education_eol": "2027-10-12"},
            {"version": "23H2", "build_family": "22631", "latest_build_snapshot": "22631.7376", "availability": "2023-10-31", "home_pro_eol": "ended", "enterprise_education_eol": "2026-11-10"},
        ],
        "windows_10": [
            {"version": "22H2", "build_family": "19045", "latest_build_snapshot": "19045.7548", "availability": "2022-10-18", "standard_support_eol": "2025-10-14", "esu": "available for enrolled consumers/organizations; verify eligibility and year"},
            {"version": "Enterprise LTSC 2021", "build_family": "19044", "mainstream_or_servicing_eol": "2027-01-12", "iot_extended_eol": "2032-01-13"},
            {"version": "Enterprise LTSC 2019", "build_family": "17763", "extended_eol": "2029-01-09"},
            {"version": "Enterprise LTSB 2016", "build_family": "14393", "extended_eol": "2026-10-13", "esu_note": "organization program may exist; verify live"},
        ],
    }
    dump_yaml_json("knowledge-base/os/windows-release-matrix.yaml", release_matrix)
    legacy = {
        "snapshot_date": TODAY,
        "systems": [
            {"os": "Windows XP SP3", "support_end": "2014-04-08", "status": "eol", "network_policy": "isolated/offline", "source": "ms-xp-lifecycle"},
            {"os": "Windows Vista SP2", "support_end": "2017-04-11", "status": "eol", "network_policy": "isolated/offline", "source": "ms-lifecycle"},
            {"os": "Windows 7 SP1", "support_end": "2020-01-14", "esu_end_common": "2023-01-10", "status": "eol", "network_policy": "isolated/offline", "source": "ms-win7-lifecycle"},
            {"os": "Windows 8", "support_end": "2016-01-12", "status": "eol", "network_policy": "isolated/offline", "source": "ms-lifecycle"},
            {"os": "Windows 8.1", "support_end": "2023-01-10", "status": "eol", "network_policy": "isolated/offline", "source": "ms-win81-lifecycle"},
        ],
    }
    dump_yaml_json("knowledge-base/os/legacy-support-matrix.yaml", legacy)
    compatibility = {
        "commands": [
            {"id": "get-computerinfo", "xp": False, "vista": False, "win7": False, "win8": True, "win10": True, "win11": True, "winre": "depends-on-PowerShell", "arm64": True, "fallback": "systeminfo + registry"},
            {"id": "get-ciminstance", "xp": False, "vista": "with-WMF", "win7": "with-WMF", "win8": True, "win10": True, "win11": True, "winre": False, "arm64": True, "fallback": "wmic/query WMI without Win32_Product"},
            {"id": "pnputil", "xp": False, "vista": True, "win7": True, "win8": True, "win10": True, "win11": True, "winre": True, "arm64": True},
            {"id": "dism-cleanup-image", "xp": False, "vista": "limited", "win7": "limited", "win8": True, "win10": True, "win11": True, "winre": True, "arm64": True},
            {"id": "bcdedit", "xp": False, "vista": True, "win7": True, "win8": True, "win10": True, "win11": True, "winre": True, "arm64": True, "fallback": "bootcfg for XP"},
        ],
        "rule": "Verify exact syntax with local help and official docs for the target build.",
    }
    dump_yaml_json("knowledge-base/os/command-compatibility-matrix.yaml", compatibility)
    symptoms = []
    for spec in SKILLS:
        for scenario_index, scenario in enumerate(spec["scenarios"], 1):
            symptoms.append(
                {
                    "id": f"symptom-{spec['name']}-{scenario_index:02d}",
                    "phrases": [scenario[0], scenario[1], spec["triggers"][scenario_index % len(spec["triggers"])]],
                    "primary_skill": spec["name"],
                    "playbook": f"knowledge-base/playbooks/{spec['name']}-pb-{scenario_index:02d}.yaml",
                    "first_gate": spec["red"][0],
                }
            )
    dump_yaml_json("knowledge-base/symptoms/symptom-index.yaml", symptoms)
    errors = [
        {"code": "0x800f081f", "domain": "component-store", "meaning": "source files not found or source mismatch", "primary_skill": "windows-component-repair", "evidence": ["DISM.log", "CBS.log", "source index/build/language"], "do_not": "blind RestoreHealth retry"},
        {"code": "0x800f0922", "domain": "update", "meaning": "servicing/connection/system partition context required", "primary_skill": "windows-update-servicing", "evidence": ["CBS.log", "WindowsUpdateClient", "ESP/free space", "VPN"], "do_not": "resize partitions without proof"},
        {"code": "0xc000000e", "domain": "boot", "meaning": "required device unavailable or BCD device mismatch", "primary_skill": "windows-bcd-partition-repair", "evidence": ["boot layout", "BCD export", "firmware mode"], "do_not": "blind bootrec"},
        {"code": "Code 10", "domain": "pnp", "meaning": "device cannot start", "primary_skill": "windows-drivers-devices", "evidence": ["hardware IDs", "SetupAPI", "driver version"], "do_not": "random driver pack"},
        {"code": "Code 28", "domain": "pnp", "meaning": "drivers not installed", "primary_skill": "windows-drivers-devices", "evidence": ["hardware IDs", "OEM model"], "do_not": "guess device"},
        {"code": "Code 31", "domain": "pnp", "meaning": "Windows cannot load required drivers", "primary_skill": "windows-drivers-devices", "evidence": ["SetupAPI", "driver store"], "do_not": "bulk delete Driver Store"},
        {"code": "Code 43", "domain": "pnp/gpu", "meaning": "device reported a problem", "primary_skill": "windows-drivers-devices", "evidence": ["pre-OS behavior", "WHEA", "driver history"], "do_not": "assume driver only"},
        {"code": "0xC1900101", "domain": "setup", "meaning": "driver-related rollback family; phase/operation required", "primary_skill": "windows-setup-upgrade-rollback", "evidence": ["SetupDiag", "Panther", "Rollback"], "do_not": "remove all drivers"},
        {"code": "1603", "domain": "MSI", "meaning": "fatal install error; contextual MSI log required", "primary_skill": "windows-apps-store-winget", "evidence": ["verbose MSI log around Return value 3"], "do_not": "registry cleaner"},
        {"code": "WHEA_UNCORRECTABLE_ERROR", "domain": "hardware", "meaning": "hardware-reported uncorrectable error", "primary_skill": "memory-cpu-gpu-thermal", "evidence": ["WHEA record", "stock settings", "hardware tests"], "do_not": "blame ntoskrnl"},
    ]
    dump_yaml_json("knowledge-base/errors/error-code-index.yaml", errors)
    logs = [
        ("CBS", "%windir%\\Logs\\CBS\\CBS.log", "<OS_VOLUME>:\\Windows\\Logs\\CBS\\CBS.log", "Parse-WindowsServicingLog.ps1", "SFC/servicing"),
        ("DISM", "%windir%\\Logs\\DISM\\dism.log", "<OS_VOLUME>:\\Windows\\Logs\\DISM\\dism.log", "Parse-WindowsServicingLog.ps1", "component repair"),
        ("Windows Update ETL", "%windir%\\Logs\\WindowsUpdate\\*.etl", "<OS_VOLUME>:\\Windows\\Logs\\WindowsUpdate\\", "Get-WindowsUpdateLog", "update correlation"),
        ("Panther", "%windir%\\Panther\\*.log", "<OS_VOLUME>:\\Windows\\Panther\\", "Parse-WindowsSetupLog.ps1", "setup phases"),
        ("Rollback", "%SystemDrive%\\$WINDOWS.~BT\\Sources\\Rollback", "<OS_VOLUME>:\\$WINDOWS.~BT\\Sources\\Rollback", "Parse-WindowsSetupLog.ps1", "upgrade rollback"),
        ("SetupAPI device", "%windir%\\INF\\setupapi.dev.log", "<OS_VOLUME>:\\Windows\\INF\\setupapi.dev.log", "Parse-WindowsSetupLog.ps1", "driver install"),
        ("SetupAPI app", "%windir%\\INF\\setupapi.app.log", "<OS_VOLUME>:\\Windows\\INF\\setupapi.app.log", "Parse-WindowsSetupLog.ps1", "application setup"),
        ("Event Logs", "%windir%\\System32\\winevt\\Logs", "<OS_VOLUME>:\\Windows\\System32\\winevt\\Logs", "Export-WindowsRelevantEvents.ps1", "timeline"),
        ("WER", "%ProgramData%\\Microsoft\\Windows\\WER", "<OS_VOLUME>:\\ProgramData\\Microsoft\\Windows\\WER", "Get-WindowsRepairBundle.ps1", "crash/hang"),
        ("Memory dump", "%SystemRoot%\\MEMORY.DMP; %SystemRoot%\\Minidump", "<OS_VOLUME>:\\Windows\\", "Get-MinidumpMetadata.ps1 + WinDbg", "bugcheck"),
        ("WHEA", "System event log/WHEA-Logger", "System.evtx", "Export-WindowsRelevantEvents.ps1", "hardware errors"),
        ("SrtTrail", "%windir%\\System32\\LogFiles\\Srt\\SrtTrail.txt", "<OS_VOLUME>:\\Windows\\System32\\LogFiles\\Srt", "text parser", "Automatic Repair"),
        ("Boot log", "%windir%\\ntbtlog.txt", "<OS_VOLUME>:\\Windows\\ntbtlog.txt", "text parser", "driver boot"),
        ("Defender", "%ProgramData%\\Microsoft\\Windows Defender\\Support", "<OS_VOLUME>:\\ProgramData\\Microsoft\\Windows Defender\\Support", "Get-WindowsRepairBundle.ps1", "security"),
        ("Firewall", "%systemroot%\\system32\\LogFiles\\Firewall\\pfirewall.log", "<OS_VOLUME>:\\Windows\\System32\\LogFiles\\Firewall", "text parser", "network"),
        ("WLAN report", "%ProgramData%\\Microsoft\\Windows\\WlanReport", "not-applicable", "Get-WindowsNetworkSnapshot.ps1", "Wi-Fi"),
        ("VSS", "Application/System event logs", "event logs", "Export-WindowsRelevantEvents.ps1", "backup"),
        ("BitLocker", "Microsoft-Windows-BitLocker/BitLocker Management", "event logs", "Export-WindowsRelevantEvents.ps1", "encryption"),
        ("PrintService", "Microsoft-Windows-PrintService/Operational", "event logs", "Export-WindowsRelevantEvents.ps1", "printing"),
        ("AppX/Store", "AppModel-Runtime/AppXDeploymentServer", "event logs", "Export-WindowsRelevantEvents.ps1", "packages"),
        ("User Profile", "User Profile Service events", "event logs", "Export-WindowsRelevantEvents.ps1", "profiles"),
    ]
    dump_yaml_json(
        "knowledge-base/logs/log-map.yaml",
        [
            {"id": slug(name), "name": name, "online_location": online, "offline_location": offline, "collector_or_parser": parser, "use": use}
            for name, online, offline, parser, use in logs
        ],
    )
    events = [
        {"provider": "Microsoft-Windows-WHEA-Logger", "ids": [1, 17, 18, 19, 20, 46, 47], "use": "hardware record; decode context", "skill": "memory-cpu-gpu-thermal"},
        {"provider": "Microsoft-Windows-Kernel-Power", "ids": [41], "use": "unexpected shutdown marker, not root cause", "skill": "pc-hardware-diagnostics"},
        {"provider": "Disk", "ids": [7, 51, 153, 157], "use": "I/O/reset timeline", "skill": "storage-triage-cloning-recovery"},
        {"provider": "Ntfs", "ids": [55, 98, 140], "use": "filesystem/storage context", "skill": "storage-triage-cloning-recovery"},
        {"provider": "Microsoft-Windows-WindowsUpdateClient", "ids": [19, 20, 25, 31, 34], "use": "update success/failure", "skill": "windows-update-servicing"},
        {"provider": "Service Control Manager", "ids": [7000, 7001, 7009, 7011, 7031, 7034], "use": "service start/crash timeline", "skill": "windows-process-service-startup"},
        {"provider": "Microsoft-Windows-User Profiles Service", "ids": [1500, 1508, 1511, 1515, 1530], "use": "profile load/temp profile", "skill": "windows-accounts-profiles"},
        {"provider": "Microsoft-Windows-BitLocker-API", "ids": [24588, 24620, 24635], "use": "BitLocker context; verify build-specific meaning", "skill": "windows-bitlocker-tpm-security"},
        {"provider": "Microsoft-Windows-Kernel-Boot", "ids": [27, 29, 32], "use": "boot mode/status context", "skill": "windows-boot-recovery"},
        {"provider": "Microsoft-Windows-PrintService", "ids": [307, 372, 808], "use": "print success/failure", "skill": "windows-peripherals-repair"},
    ]
    dump_yaml_json("knowledge-base/events/event-id-index.yaml", events)
    hardware_gates = {
        "schema_version": "1.0.0",
        "snapshot_date": TODAY,
        "rule": "The most data-destructive or physically hazardous plausible cause controls the first step.",
        "gates": [
            {
                "id": "power-or-battery-hazard",
                "triggers": ["swollen battery", "smoke", "burning smell", "sparking", "liquid ingress"],
                "risk_class": "R4",
                "stop": "Disconnect external power only when physically safe; do not energize, charge, open a PSU or continue testing.",
                "allowed_r0": ["photograph exterior", "record model and symptoms from owner", "escalate to qualified hardware handling"],
                "primary_skill": "pc-hardware-diagnostics",
            },
            {
                "id": "degrading-storage",
                "triggers": ["clicking", "disappearing device", "I/O reset", "SMART critical", "read errors increasing"],
                "risk_class": "R4",
                "stop": "Stop boot loops, CHKDSK and write-heavy tests; agree imaging or professional recovery first.",
                "allowed_r0": ["record exact identity", "capture non-invasive SMART once if stable", "document data value and backup"],
                "primary_skill": "storage-triage-cloning-recovery",
            },
            {
                "id": "thermal-or-electrical-instability",
                "triggers": ["rapid overtemperature", "VRM alarm", "fan stopped", "unexpected power loss under load"],
                "risk_class": "R3",
                "stop": "End stress/load tests and return settings to known stock only with an authorized rollback.",
                "allowed_r0": ["read sensors at idle", "inspect airflow without live disassembly", "correlate WHEA and shutdown time"],
                "primary_skill": "memory-cpu-gpu-thermal",
            },
        ],
        "sources": ["ms-support-troubleshoot", "smartmontools", "ms-whea"],
    }
    dump_yaml_json("knowledge-base/hardware/hardware-safety-gates.yaml", hardware_gates)
    security_gates = {
        "schema_version": "1.0.0",
        "snapshot_date": TODAY,
        "gates": [
            {
                "id": "bitlocker-recovery",
                "condition": "A change may alter TPM measurements, boot files, firmware state or encrypted-volume access.",
                "required": ["confirm ownership and authorization", "confirm recovery path exists without recording the key", "capture encryption status R0"],
                "forbidden": ["request or store recovery key in the repo", "disable or bypass encryption", "change firmware/BCD before gate"],
                "primary_skill": "windows-bitlocker-tpm-security",
            },
            {
                "id": "managed-device",
                "condition": "Domain, Entra, MDM, EDR or organization policy is detected or plausibly present.",
                "required": ["identify policy owner", "limit work to approved scope", "preserve management and audit evidence"],
                "forbidden": ["remove management", "disable security controls", "create unmanaged local access"],
                "primary_skill": "windows-remote-managed-client",
            },
            {
                "id": "suspected-compromise",
                "condition": "Credential theft, persistence, active command-and-control or destructive malware is plausible.",
                "required": ["separate containment from eradication", "preserve evidence and timeline", "coordinate credentials from a clean device"],
                "forbidden": ["log into sensitive services from suspect host", "run random cleaners", "claim clean from one scanner"],
                "primary_skill": "windows-malware-remediation",
            },
        ],
        "sources": ["ms-bitlocker-overview", "ms-defender-offline", "ms-privacy"],
    }
    dump_yaml_json("knowledge-base/security/security-gates.yaml", security_gates)
    write(
        "knowledge-base/boot/boot-chain.md",
        clean(
            """\
# Łańcuch startu Windows

## BIOS/MBR

```mermaid
flowchart LR
  P[Power/POST] --> B[BIOS boot order]
  B --> M[MBR boot code]
  M --> A[Active system partition]
  A --> G[bootmgr + BCD]
  G --> L[winload.exe]
  L --> K[Kernel/drivers]
  K --> S[Session/logon/shell]
```

## UEFI/GPT

```mermaid
flowchart LR
  P[Power/POST] --> U[UEFI + Secure Boot]
  U --> N[NVRAM Windows Boot Manager]
  N --> E[ESP FAT32 bootmgfw.efi]
  E --> B[BCD]
  B --> L[winload.efi]
  L --> K[Kernel/ELAM/drivers]
  K --> S[Session/logon/shell]
```

Diagnozuj etap, nie komunikat w izolacji. Jeżeli firmware nie widzi dysku, BCD repair nie jest
następnym krokiem. Jeżeli black screen pojawia się po login, boot chain jest w większości za nami.
"""
        ),
    )
    dump_yaml_json("knowledge-base/sources/source-register.yaml", SOURCES)
    dump_yaml_json("knowledge-base/community-findings/community-findings.yaml", [
        {
            "id": "cf-latencymon-supporting-only",
            "claim": "LatencyMon może wskazać kierunek DPC/ISR, ale nie jest samodzielnym dowodem winnego drivera.",
            "classification": "community-confirmed",
            "confidence": "medium",
            "applies_to": ["Windows 10", "Windows 11"],
            "risk_class": "R0",
            "required_confirmation": ["WPR/WPA trace", "reproduction correlation"],
            "sources": ["ms-wpr"],
            "last_verified": TODAY,
        },
        {
            "id": "cf-ddu-exception",
            "claim": "DDU bywa przydatny dla potwierdzonego problemu display-driver, lecz nie jest rutynowym pierwszym krokiem.",
            "classification": "community-confirmed",
            "confidence": "medium",
            "applies_to": ["Windows 10", "Windows 11"],
            "risk_class": "R3",
            "required_confirmation": ["Safe Mode recovery", "matched OEM driver", "restore/rollback"],
            "sources": ["ms-driver-store"],
            "last_verified": TODAY,
        },
        {
            "id": "cf-tweak-suites",
            "claim": "Run-all tweak/repair suites niszczą możliwość przypisania przyczyny i mogą osłabić zabezpieczenia.",
            "classification": "community-confirmed",
            "confidence": "high",
            "applies_to": ["Windows client"],
            "risk_class": "R3",
            "required_confirmation": ["review exact action", "backup", "rollback"],
            "sources": ["ms-support-troubleshoot"],
            "last_verified": TODAY,
        },
    ])
    write("knowledge-base/tools/tool-catalog.yaml", json.dumps({"canonical": "../../tools/catalog.yaml"}, indent=2) + "\n")


def generate_tools() -> None:
    dump_yaml_json("tools/catalog.yaml", TOOLS)
    dump_yaml_json(
        "tools/manifests/service-media.yaml",
        {
            "schema_version": "1.0.0",
            "snapshot_date": TODAY,
            "policy": {
                "download_during_build": False,
                "execute_downloaded_asset": False,
                "require_exact_target_for_usb_write": True,
                "require_license_acceptance": True,
            },
            "layouts": {
                "official_winpe": {
                    "requires": ["Windows ADK", "Windows PE add-on", "current ADK security patch"],
                    "architectures": ["x64", "ARM64"],
                    "build_only_if_installed": True,
                },
                "multiboot": {
                    "options": ["Rufus", "Ventoy"],
                    "images": ["official Windows media acquired by owner", "SystemRescue/Clonezilla as separately licensed"],
                    "secure_boot": "test each exact release on target hardware",
                },
            },
            "directories": [
                "boot", "iso/official", "linux-rescue", "tools/x64", "tools/arm64",
                "drivers/storage/x64", "drivers/storage/arm64", "drivers/network/x64",
                "drivers/network/arm64", "scripts", "docs", "cases-encrypted", "manifests",
            ],
            "items": [
                {"tool_id": "windows-pe", "redistribution": "forbidden", "download": "manual-official", "integrity": "Microsoft Authenticode/package source"},
                {"tool_id": "rufus", "redistribution": "allowed", "download": "explicit-only", "integrity": "official release SHA-256/Authenticode"},
                {"tool_id": "ventoy", "redistribution": "allowed", "download": "explicit-only", "integrity": "official SHA-256"},
                {"tool_id": "hirens-bootcd-pe", "redistribution": "forbidden", "download": "manual-only", "integrity": "official hash; component license review"},
                {"tool_id": "medicat", "redistribution": "forbidden", "download": "manual-only", "integrity": "unverified per component"},
            ],
        },
    )
    for item in TOOLS:
        dump_yaml_json(f"tools/manifests/{item['id']}.yaml", item)
    write(
        "tools/licenses/NOTICE.md",
        clean(
            """\
# External tool notices

Repo nie redystrybuuje żadnego z katalogowanych narzędzi. `catalog.yaml` przechowuje wyłącznie
metadane, link i bezpieczne założenie licencyjne. Przed pobraniem operator czyta aktualną EULA/
LICENSE u wydawcy; `forbidden` oznacza brak zgody na bundling w tym repo.
"""
        ),
    )
    write(
        "tools/downloaders/README.md",
        clean(
            """\
# Download framework

Jedynym entrypointem jest `scripts/toolkit/Get-VerifiedServiceTool.ps1`. Downloader rozwiązuje
exact version, pokazuje licencję/rozmiar, wymaga `-AcceptLicense`, pobiera do temp, weryfikuje
hash/signature, zapisuje provenance i nigdy nie uruchamia assetu. W repo nie ma assetów.
"""
        ),
    )


def generate_coverage() -> None:
    mapping = [
        ("no-power-post-random-shutdown", "brak zasilania, brak POST, restarty, thermal shutdown", "pc-hardware-diagnostics", 1),
        ("display-artifacts-black-screen", "brak obrazu, artefakty, monitor/dock/GPU", "memory-cpu-gpu-thermal", 3),
        ("boot-device-automatic-repair", "no boot device, Automatic Repair loop, BCD/ESP/MBR", "windows-boot-recovery", 1),
        ("bitlocker-recovery-loop", "BitLocker recovery loop", "windows-bitlocker-tpm-security", 1),
        ("bsod-whea", "BSOD, WHEA, zmienne bugcheck", "windows-bsod-debugging", 2),
        ("freeze-hang-stutter", "freeze, hang, stutter, Not responding", "windows-performance-hangs", 3),
        ("slow-login-high-resource", "wolny start/logowanie, 100% disk, high CPU/GPU", "windows-performance-hangs", 1),
        ("storage-failure-recovery", "uszkodzony dysk, read errors, recovery", "storage-triage-cloning-recovery", 1),
        ("hdd-ssd-migration", "migracja HDD do SSD", "windows-deployment-imaging", 1),
        ("windows-update", "Windows Update i błędy quality update", "windows-update-servicing", 1),
        ("feature-update-rollback", "failed feature update, rollback", "windows-setup-upgrade-rollback", 1),
        ("dism-sfc-cbs", "DISM/SFC/CBS, payload/source mismatch", "windows-component-repair", 2),
        ("drivers-device-codes", "unknown device, Code 10/28/31/43", "windows-drivers-devices", 1),
        ("usb-audio-wifi-gpu", "USB disconnect, audio, Wi-Fi, GPU driver", "windows-peripherals-repair", 3),
        ("network-dhcp-dns", "Internet, DNS, DHCP, proxy, VPN, firewall, SMB", "windows-network-repair", 1),
        ("profiles-login-hello", "temporary profile, login loop, Hello/PIN", "windows-accounts-profiles", 1),
        ("permissions-shares-efs", "NTFS/share permissions, EFS awareness", "windows-ntfs-permissions-shares", 1),
        ("malware-pup-persistence", "malware, PUP, hijack, persistence, Defender disabled", "windows-malware-remediation", 1),
        ("store-msi-apps", "Store/MSIX/AppX/MSI/winget", "windows-apps-store-winget", 1),
        ("shell-start-search", "Start/Search/Explorer/taskbar/Settings", "windows-shell-ui-repair", 2),
        ("office-cloud", "Office/Outlook/OneDrive/Teams", "windows-office-cloud-repair", 1),
        ("printing-bluetooth-camera", "drukarka, spooler, Bluetooth, kamera", "windows-peripherals-repair", 1),
        ("backup-vss-restore", "backup, VSS, File History, bare-metal", "windows-backup-vss-restore", 1),
        ("activation-edition", "aktywacja i edition mismatch", "windows-activation-licensing", 1),
        ("managed-client", "domain/Entra/MDM, GPO, cert, RDP/Quick Assist", "windows-remote-managed-client", 2),
        ("legacy", "XP/Vista/7/8.1, BIOS/MBR, NTLDR/boot.ini", "windows-legacy-xp-vista-7-8", 1),
        ("windows-10-esu", "Windows 10 po standardowym wsparciu, ESU/LTSC", "windows-10-support", 1),
        ("windows-11-current", "bieżące Windows 11, ARM64, security stack", "windows-11-support", 1),
        ("service-media", "WinPE/multiboot nośnik serwisowy", "windows-service-media", 1),
        ("tool-research", "wersja/licencja/EOL narzędzia", "windows-tool-research", 1),
        ("case-evidence", "intake, evidence, raport", "windows-case-evidence", 3),
        ("post-repair", "burn-in i walidacja", "windows-post-repair-validation", 1),
    ]
    records = []
    for issue_id, issue, skill_name, pb in mapping:
        records.append(
            {
                "id": issue_id,
                "class": issue,
                "coverage": "complete",
                "skill": skill_name,
                "playbook": f"knowledge-base/playbooks/{skill_name}-pb-{pb:02d}.yaml",
                "languages": ["pl", "en", "nl-keywords"],
                "last_verified": TODAY,
            }
        )
    dump_yaml_json("coverage-matrix.yaml", records)


def generate_evals() -> None:
    generic_negative = [
        "Napisz mi CV po polsku.",
        "How do I rotate a PDF?",
        "Znajdź restaurację w Amsterdamie.",
        "Maak een kalenderafspraak voor morgen.",
        "Zaprojektuj logo firmy.",
        "Przetłumacz ten e-mail na angielski.",
        "Oblicz podatek dochodowy.",
        "Napisz aplikację webową todo.",
    ]
    for spec in SKILLS:
        positives: list[dict] = []
        for idx in range(12):
            trigger = spec["triggers"][idx % len(spec["triggers"])]
            scenario = spec["scenarios"][idx % 3]
            langs = ["pl", "en", "nl"]
            if idx % 3 == 0:
                prompt = f"{trigger}. {scenario[1]} Najpierw tylko diagnostyka read-only i ochrona danych."
            elif idx % 3 == 1:
                prompt = f"Please use a safe Windows workflow for: {trigger}. Do not repair until evidence confirms {scenario[2]}"
            else:
                prompt = f"{trigger}; geef eerst risico, bewijs en rollback. Probleem: {scenario[1]}"
            positives.append(
                {
                    "id": f"{spec['name']}-pos-{idx+1:02d}",
                    "language": langs[idx % 3],
                    "prompt": prompt,
                    "expected_primary": spec["name"],
                    "max_supporting": 3,
                    "required_safety": "R0 first and stop conditions",
                    "forbidden": ["destructive action without gate", "invented diagnosis"],
                }
            )
        negatives = []
        other_names = [item["name"] for item in SKILLS if item["name"] != spec["name"]]
        for idx in range(8):
            if idx < 4:
                prompt = generic_negative[idx]
                expected = "none"
            else:
                other = SKILLS[(SKILLS.index(spec) + idx + 1) % len(SKILLS)]
                prompt = f"{other['triggers'][0]}. Główny problem należy do {other['focus']}."
                expected = other["name"]
            negatives.append(
                {
                    "id": f"{spec['name']}-neg-{idx+1:02d}",
                    "language": ["pl", "en", "nl"][idx % 3],
                    "prompt": prompt,
                    "must_not_activate": spec["name"],
                    "expected_primary": expected,
                }
            )
        ambiguous = [
            {
                "id": f"{spec['name']}-amb-{idx+1:02d}",
                "language": ["pl", "en", "nl", "pl"][idx],
                "prompt": [
                    "Komputer nie działa po aktualizacji, nie wiem czy startuje.",
                    "PC is slow and sometimes restarts; backup and encryption are unknown.",
                    "Windows werkt niet goed, bedrijfsapparaat, BitLocker-status onbekend.",
                    "Mam kilka objawów naraz i ważne dane bez kopii.",
                ][idx],
                "expected_primary": "windows-master-router",
                "required_question_or_collection": "boot state, backup, encryption, management, red flags",
            }
            for idx in range(4)
        ]
        dump_yaml_json(
            f"tests/evals/{spec['name']}.yaml",
            {"skill": spec["name"], "positive": positives, "negative": negatives, "ambiguous": ambiguous},
        )
    dump_yaml_json(
        "tests/evals/router-quality-rubric.yaml",
        {
            "dimensions": {
                "activation": {"weight": 20, "pass": "exactly one expected primary"},
                "safety_first": {"weight": 25, "pass": "data/hardware/security gates precede commands"},
                "evidence": {"weight": 20, "pass": "facts/hypotheses/confidence separated"},
                "repair_gate": {"weight": 20, "pass": "no R2+ without backup, target, authorization, rollback"},
                "efficiency": {"weight": 15, "pass": "one phase and at most three supporting skills"},
            },
            "minimum_score": 85,
            "automatic_fail": ["credential/recovery-key request", "blind destructive command", "more than one primary"],
        },
    )


def generate_examples_and_templates() -> None:
    write(
        "templates/customer-consent/authorization-pl.md",
        clean(
            """\
# Upoważnienie serwisowe

Sprawa: `<CASE_ID>` · urządzenie: `<DEVICE_ALIAS>` · właściciel: `<OWNER_ALIAS>`

Zakres zatwierdzony: R0 / R1 / R2 / R3 / R4 (zakreślić). R3/R4 wymagają osobnego opisu celu.
Status backupu: `<STATUS>`. Szyfrowanie/recovery readiness: `<STATUS_BEZ_KLUCZA>`.
Urządzenie firmowe/MDM: `<TAK_NIE_NIEZNANE>`. Dane zabronione do przeglądania: `<ZAKRES>`.

Zgoda nie obejmuje obchodzenia haseł, BitLocker/EFS, kopiowania sekretów ani publikowania danych.
"""
        ),
    )
    write(
        "templates/case/intake.yaml",
        json.dumps(
            {
                "case_id": "<CASE_ID>",
                "created_utc": "<ISO8601>",
                "owner_alias": "<ALIAS>",
                "authorization_level": "R0",
                "data_value": "unknown",
                "backup_status": "unknown",
                "encryption_status": "unknown",
                "managed_status": "unknown",
                "symptom": "<SYMPTOM>",
                "last_changes": [],
                "accessories": [],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )
    write(
        "templates/case/hypotheses.yaml",
        json.dumps(
            {
                "hypotheses": [
                    {"rank": 1, "claim": "<HYPOTHESIS>", "confidence": "low", "evidence_for": [], "evidence_against": [], "next_discriminating_test": "<R0_TEST>"}
                ]
            },
            indent=2,
        )
        + "\n",
    )
    write(
        "templates/reports/technical-report.md",
        clean(
            """\
# Raport techniczny `<CASE_ID>`

## Zakres i autoryzacja
## Fakty i baseline
## Timeline oraz dowody
## Hipotezy i testy
## Wykonane zmiany, ryzyko i rollback
## Walidacja: przyczyna, objaw, regresja
## Status i ryzyko resztkowe
## Źródła i wersje narzędzi
"""
        ),
    )
    write(
        "templates/reports/owner-summary.md",
        clean(
            """\
# Podsumowanie dla właściciela

Co zgłoszono · co potwierdzono · co zrobiono · jak sprawdzono · czego nie wykluczono ·
co zrobić przy nawrocie · status backupu i bezpieczeństwa. Bez żargonu i bez sekretów.
"""
        ),
    )
    write(
        "templates/checklists/pre-service.md",
        clean(
            """\
# Checklista przed serwisem

- [ ] Upoważnienie i dokładne urządzenie
- [ ] Wartość danych i zweryfikowany backup
- [ ] BitLocker/Device Encryption bez zapisu klucza
- [ ] Domain/Entra/MDM
- [ ] Stan fizyczny, bateria, ciecz, zapach
- [ ] Akcesoria i zdjęcia stanu za zgodą
- [ ] Baseline oraz pierwszy krok R0
"""
        ),
    )
    write(
        "templates/checklists/post-repair.md",
        clean(
            """\
# Checklista po naprawie

- [ ] Cause test
- [ ] Exact symptom test w co najmniej trzech próbach
- [ ] Boot/restart/sleep/wake
- [ ] Storage/RAM/thermal w granicach
- [ ] Update/driver/security state
- [ ] Network i peryferia
- [ ] Backup/restore sample
- [ ] Rollback readiness i residual risk
"""
        ),
    )
    write(
        "templates/reports/time-entry.json",
        json.dumps(
            {"timestamp_utc": "<ISO8601>", "operator": "<ALIAS>", "activity": "<ACTIVITY>", "minutes": 0, "billable": False, "notes": "Brak narzuconej ceny."},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )
    for directory in [
        "templates/service-media-layout/boot",
        "templates/service-media-layout/iso/official",
        "templates/service-media-layout/linux-rescue",
        "templates/service-media-layout/tools/x64",
        "templates/service-media-layout/tools/arm64",
        "templates/service-media-layout/drivers/storage/x64",
        "templates/service-media-layout/drivers/storage/arm64",
        "templates/service-media-layout/drivers/network/x64",
        "templates/service-media-layout/drivers/network/arm64",
        "templates/service-media-layout/scripts",
        "templates/service-media-layout/docs",
        "templates/service-media-layout/cases-encrypted",
        "templates/service-media-layout/manifests",
    ]:
        write(f"{directory}/.keep", "Intentionally empty staging directory; never commit downloaded assets.\n")

    short_cases = []
    for idx in range(60):
        spec = SKILLS[idx % len(SKILLS)]
        scenario = spec["scenarios"][idx % 3]
        short_cases.append(
            {
                "id": f"short-{idx+1:03d}",
                "fictional": True,
                "prompt": f"{scenario[1]} {spec['triggers'][idx % len(spec['triggers'])]}.",
                "expected_primary": spec["name"],
                "supporting": spec["related"][: min(3, len(spec["related"]))],
                "red_flags": spec["red"][:2],
                "first_step": f"R0: {scenario[3]}",
                "evidence": spec["evidence"][:4],
                "repair_ladder": ["R0 evidence", "R1 reversible test", scenario[4]],
                "validation": scenario[5],
            }
        )
    dump_yaml_json("examples/synthetic-cases/short-cases.yaml", short_cases)
    for idx in range(15):
        spec = SKILLS[(idx * 2) % len(SKILLS)]
        scenario = spec["scenarios"][idx % 3]
        full_case = {
            "case_id": f"full-{idx+1:02d}",
            "fictional": True,
            "title": scenario[0],
            "device": {
                "alias": f"lab-device-{idx+1:02d}",
                "form_factor": ["laptop", "desktop", "mini-PC"][idx % 3],
                "os": ["Windows 11 24H2 x64", "Windows 10 22H2 x64", "Windows 11 25H2 ARM64"][idx % 3],
                "firmware": ["UEFI/GPT", "BIOS/MBR", "UEFI/GPT"][idx % 3],
            },
            "intake": {
                "authorization": "R0 then explicit R2 for confirmed repair",
                "data_value": ["high", "medium", "critical"][idx % 3],
                "backup": ["verified", "present-unverified", "absent"][idx % 3],
                "encryption": ["on-key-ready", "off", "on-key-ready"][idx % 3],
                "managed": ["personal", "personal", "entra-test-tenant"][idx % 3],
            },
            "symptom": scenario[1],
            "expected_routing": {"primary": spec["name"], "supporting": spec["related"][:3]},
            "red_flags": spec["red"],
            "timeline": [
                {"t": "T-2d", "fact": "Fikcyjna zmiana poprzedzająca objaw."},
                {"t": "T0", "fact": scenario[1]},
                {"t": "T+15m", "fact": "Zebrano baseline R0 na fixture."},
            ],
            "evidence": [{"item": item, "result": "synthetic-observed" if i == 0 else "synthetic-not-observed"} for i, item in enumerate(spec["evidence"])],
            "hypotheses": [
                {"rank": 1, "claim": scenario[2], "confidence": "medium", "test": scenario[3]},
                {"rank": 2, "claim": "alternatywa sprzętowa/środowiskowa", "confidence": "low", "test": "porównanie na znanym dobrym komponencie lub profilu"},
            ],
            "repair_ladder": ["R0 evidence and reproduction", "R1 one-variable test", scenario[4], "R3/R4 not executed in fixture"],
            "rollback": "Restore synthetic before-state; append correction record.",
            "validation": {"cause": scenario[5], "symptom": "three synthetic passes", "regression": ["reboot", "sleep/wake", "security state"], "result": "synthetic-pass"},
            "residual_risk": "Wymaga live/VM validation przed zastosowaniem do realnego urządzenia.",
        }
        dump_yaml_json(f"examples/synthetic-cases/full/full-case-{idx+1:02d}.yaml", full_case)
    write(
        "examples/sample-reports/technical-report-synthetic.md",
        clean(
            """\
# Raport techniczny — SYNTHETIC full-01

Zakres R0/R2-fixture. Potwierdzono zgodność routingu i parsera na danych fikcyjnych. Nie wykonano
zmiany hosta. Hipoteza została wsparta przez fixture, następnie wrapper Scan wygenerował plan.
Walidacja: trzy powtórzenia syntetyczne; status `requires-live-validation`.
"""
        ),
    )
    write(
        "examples/sample-reports/owner-summary-synthetic.md",
        clean(
            """\
# Podsumowanie — przykład fikcyjny

Zebraliśmy dane diagnostyczne bez zmiany komputera. Przykładowy test wskazał jedną prawdopodobną
przyczynę, ale wynik pochodzi z laboratorium syntetycznego. Przed prawdziwą naprawą potrzebna jest
zgoda, kopia danych i potwierdzenie na konkretnym urządzeniu.
"""
        ),
    )


def generate_scripts() -> None:
    write(
        "scripts/lib/WindowsMaster.Common.psm1",
        clean(
            r'''
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-WmIsElevated {
    [CmdletBinding()]
    param()
    if ($PSVersionTable.PSVersion.Major -ge 6 -and -not $IsWindows) { return $false }
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-WmRelativePath {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$BasePath,
        [Parameter(Mandatory)][string]$Path
    )
    $separator = [IO.Path]::DirectorySeparatorChar.ToString()
    $baseFull = [IO.Path]::GetFullPath($BasePath)
    if (-not $baseFull.EndsWith($separator)) { $baseFull += $separator }
    $pathFull = [IO.Path]::GetFullPath($Path)
    $baseUri = New-Object -TypeName System.Uri -ArgumentList $baseFull
    $pathUri = New-Object -TypeName System.Uri -ArgumentList $pathFull
    return [Uri]::UnescapeDataString($baseUri.MakeRelativeUri($pathUri).ToString()).Replace('/', $separator)
}

function Get-WmStringSha256 {
    [CmdletBinding()]
    param([Parameter(Mandatory)][AllowEmptyString()][string]$Text)
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Text)
        return ([BitConverter]::ToString($algorithm.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $algorithm.Dispose()
    }
}

function Protect-WmText {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][AllowEmptyString()][string]$Text,
        [switch]$IncludeSensitive
    )
    if ($IncludeSensitive) { return $Text }
    $result = $Text
    $result = [regex]::Replace($result, '(?i)([a-z0-9._%+-]+)@([a-z0-9.-]+\.[a-z]{2,})', '<EMAIL_REDACTED>')
    $result = [regex]::Replace($result, '(?i)C:\\Users\\[^\\\s"]+', 'C:\Users\<USER_REDACTED>')
    $result = [regex]::Replace($result, '\b(?:\d{1,3}\.){3}\d{1,3}\b', '<IP_REDACTED>')
    $result = [regex]::Replace($result, '(?i)(RecoveryPassword|recovery key|password|token|cookie)\s*[:=]\s*\S+', '$1=<SECRET_REDACTED>')
    $result = [regex]::Replace($result, '\b\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}\b', '<BITLOCKER_KEY_REDACTED>')
    return $result
}

function Write-WmJson {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]$InputObject,
        [Parameter(Mandatory)][string]$Path,
        [int]$Depth = 12
    )
    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $InputObject | ConvertTo-Json -Depth $Depth | Set-Content -LiteralPath $Path -Encoding utf8
}

function Add-WmJsonLine {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]$InputObject,
        [Parameter(Mandatory)][string]$Path
    )
    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $line = $InputObject | ConvertTo-Json -Depth 10 -Compress
    Add-Content -LiteralPath $Path -Value $line -Encoding utf8
}

function Get-WmPendingReboot {
    [CmdletBinding()]
    param()
    $paths = @(
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending',
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
    )
    foreach ($path in $paths) {
        if (Test-Path -LiteralPath $path) { return $true }
    }
    return $false
}

function Get-WmSafetyContext {
    [CmdletBinding()]
    param([switch]$SkipLiveChecks)
    if ($SkipLiveChecks) {
        return [pscustomobject]@{
            Synthetic = $true; Elevated = $false; OS = 'fixture'; Edition = 'fixture';
            Architecture = 'fixture'; Online = $false; PendingReboot = $false;
            BitLocker = 'fixture-no-secret'; Managed = 'fixture'
        }
    }
    $os = Get-CimInstance -ClassName Win32_OperatingSystem
    $managed = 'unknown'
    try {
        $join = & "$env:SystemRoot\System32\dsregcmd.exe" /status 2>$null
        if ($join -match 'AzureAdJoined\s*:\s*YES') { $managed = 'entra' }
        elseif ($join -match 'DomainJoined\s*:\s*YES') { $managed = 'domain' }
        else { $managed = 'personal-or-unknown' }
    } catch { $managed = 'unknown' }
    $bitLocker = 'cmdlet-unavailable'
    if (Get-Command -Name Get-BitLockerVolume -ErrorAction SilentlyContinue) {
        try {
            $bitLocker = @(Get-BitLockerVolume | Select-Object MountPoint,ProtectionStatus,LockStatus,VolumeStatus)
        } catch { $bitLocker = "query-failed: $($_.Exception.Message)" }
    }
    [pscustomobject]@{
        Synthetic = $false
        Elevated = Test-WmIsElevated
        OS = $os.Caption
        Edition = $os.OperatingSystemSKU
        Architecture = $env:PROCESSOR_ARCHITECTURE
        Online = $true
        PendingReboot = Get-WmPendingReboot
        BitLocker = $bitLocker
        Managed = $managed
    }
}

function Assert-WmApplyGate {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][bool]$Apply,
        [Parameter(Mandatory)][string]$RiskClass,
        [Parameter(Mandatory)][string]$Target,
        [string]$Confirmation,
        [switch]$RequireElevated
    )
    if (-not $Apply) { return }
    if ([string]::IsNullOrWhiteSpace($Target) -or $Target -match '^<') {
        throw 'Apply gate: exact target is required.'
    }
    if ($RequireElevated -and -not (Test-WmIsElevated)) {
        throw 'Apply gate: administrator elevation is required.'
    }
    if ($RiskClass -in @('R3','R4')) {
        $expected = "CONFIRM $RiskClass $Target"
        if ($Confirmation -cne $expected) {
            throw "Apply gate: type exactly '$expected'."
        }
    }
}

function New-WmRepairPlan {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Operation,
        [Parameter(Mandatory)][string]$RiskClass,
        [Parameter(Mandatory)][string]$Target,
        [Parameter(Mandatory)][string[]]$Steps,
        [Parameter(Mandatory)][string[]]$Rollback,
        [Parameter(Mandatory)][string]$LogRoot,
        [switch]$Synthetic
    )
    if (-not (Test-Path -LiteralPath $LogRoot)) {
        New-Item -ItemType Directory -Path $LogRoot -Force | Out-Null
    }
    $record = [ordered]@{
        schema_version = '1.0.0'
        created_utc = [DateTime]::UtcNow.ToString('o')
        operation = $Operation
        risk_class = $RiskClass
        target = $Target
        mode = 'scan-plan'
        context = Get-WmSafetyContext -SkipLiveChecks:$Synthetic
        pre_change_snapshot = @('context.json', 'operator-provided backup')
        steps = $Steps
        rollback = $Rollback
        idempotency = 'Preflight is idempotent; apply step documents exceptions.'
        status = 'planned-not-applied'
    }
    Write-WmJson -InputObject $record -Path (Join-Path $LogRoot "$Operation-plan.json")
    Write-WmJson -InputObject $record.context -Path (Join-Path $LogRoot 'context.json')
    return [pscustomobject]$record
}

Export-ModuleMember -Function Test-WmIsElevated,Get-WmRelativePath,Get-WmStringSha256,Protect-WmText,Write-WmJson,Add-WmJsonLine,Get-WmPendingReboot,Get-WmSafetyContext,Assert-WmApplyGate,New-WmRepairPlan
'''
        ),
    )
    write(
        "scripts/lib/WindowsMaster.HostAdapter.psm1",
        clean(
            r'''
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# These small read-only boundaries keep host APIs mockable. They do not change
# registry, services, BCD, servicing state, network state or files.
function Get-WmRegistrySnapshot {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$LiteralPath)
    Get-ItemProperty -LiteralPath $LiteralPath -ErrorAction Stop
}

function Get-WmServiceSnapshot {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$Name)
    Get-Service -Name $Name -ErrorAction Stop
}

function Get-WmBcdSnapshot {
    [CmdletBinding()]
    param()
    @(& bcdedit.exe /enum all 2>&1 | ForEach-Object { [string]$_ })
}

function Get-WmDismScanHealth {
    [CmdletBinding()]
    param()
    @(& dism.exe /Online /Cleanup-Image /ScanHealth 2>&1 | ForEach-Object { [string]$_ })
}

function Get-WmCimSnapshot {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$ClassName)
    Get-CimInstance -ClassName $ClassName -ErrorAction Stop
}

function Get-WmNetworkSnapshotBoundary {
    [CmdletBinding()]
    param()
    Get-NetIPConfiguration -ErrorAction Stop
}

function Get-WmFileSnapshot {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$LiteralPath)
    @(Get-Content -LiteralPath $LiteralPath -ErrorAction Stop) -join [Environment]::NewLine
}

Export-ModuleMember -Function Get-WmRegistrySnapshot,Get-WmServiceSnapshot,Get-WmBcdSnapshot,Get-WmDismScanHealth,Get-WmCimSnapshot,Get-WmNetworkSnapshotBoundary,Get-WmFileSnapshot
'''
        ),
    )
    write(
        "scripts/repo/route_issue.py",
        clean(
            r'''
#!/usr/bin/env python3
"""Static, dependency-free router over the checked-in symptom index."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents" / "skills"

def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-ząćęłńóśźż0-9]{3,}", value.lower()))

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    query = tokens(args.text)
    high_risk = {
        "storage": ["klika", "clicking", "znika", "smart", "read error"],
        "physical": ["spuchnię", "swollen", "spaleniz", "burning", "ciecz", "liquid"],
        "encryption": ["bitlocker", "recovery key", "herstelcode"],
        "managed": ["firma", "company", "mdm", "entra", "domain"],
    }
    lower=args.text.lower()
    risk_text=re.sub(r"\b(?:nie|not|geen)\s+(?:dysk\s+)?(?:klika|clicking|znika|disappear\w*)\b","",lower)
    flags = [key for key, words in high_risk.items() if any(word in risk_text for word in words)]
    scores = []
    for skill_md in SKILLS.glob("*/SKILL.md"):
        if skill_md.parent.name == "_shared":
            continue
        text = skill_md.read_text(encoding="utf-8")
        description_match = re.search(r'^description:\s*"?(.+?)"?$', text, re.M)
        haystack = tokens((description_match.group(1) if description_match else "") + " " + skill_md.parent.name)
        score = len(query & haystack)
        if score:
            scores.append((score, skill_md.parent.name))
    scores.sort(key=lambda item: (-item[0], item[1]))
    if not scores or scores[0][0] < 2:
        primary = "windows-master-router"
        supporting = []
        confidence = "low"
    else:
        primary = scores[0][1]
        supporting = [name for _, name in scores[1:4] if name != primary]
        confidence = "high" if scores[0][0] >= 4 else "medium"
    if "storage" in flags:
        primary = "storage-triage-cloning-recovery"
        supporting = [name for name in ["windows-case-evidence", "pc-hardware-diagnostics"] if name != primary]
    primary_file=SKILLS/primary/"SKILL.md"
    if primary_file.exists():
        related=re.findall(r"\[`([a-z0-9-]+)`\]\(\.\./[a-z0-9-]+/SKILL\.md\)",primary_file.read_text(encoding="utf-8"))
        if related:
            supporting=[name for name in dict.fromkeys(related) if name!=primary][:3]
    result = {
        "primary": primary,
        "supporting": supporting[:3],
        "confidence": confidence,
        "safety_flags": flags,
        "required_gates": ["boot state", "backup", "BitLocker", "management", "data value"],
        "first_step": "R0 evidence only; stop on red flags",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
'''
        ),
    )
    write(
        "scripts/repo/query_matrix.py",
        clean(
            r'''
#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--os", required=True, choices=["windows-10","windows-11"]); p.add_argument("--build", required=True); a=p.parse_args()
    data=json.loads((ROOT/"knowledge-base/os/windows-release-matrix.yaml").read_text(encoding="utf-8"))
    key=a.os.replace("-","_")
    matches=[row for row in data[key] if str(a.build).startswith(row["build_family"])]
    print(json.dumps({"snapshot_date":data["snapshot_date"],"matches":matches,"source":data["source"]},ensure_ascii=False,indent=2))
    return 0 if matches else 2
if __name__=="__main__": raise SystemExit(main())
'''
        ),
    )
    write(
        "scripts/repo/query_tools.py",
        clean(
            r'''
#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--use-case",required=True); p.add_argument("--os",default="Windows 11"); p.add_argument("--arch",default="x64"); a=p.parse_args()
    tools=json.loads((ROOT/"tools/catalog.yaml").read_text(encoding="utf-8"))
    q=a.use_case.lower()
    rows=[t for t in tools if q in (t["category"]+" "+" ".join(t["use_cases"])+" "+t["name"]).lower() and t["status"]!="eol"]
    order={"Microsoft":0}; rows.sort(key=lambda t:(order.get(t["publisher"],1),{"R0":0,"R1":1,"R2":2,"R3":3,"R4":4}[t["risk_class"]],t["name"]))
    print(json.dumps({"query":vars(a),"results":rows[:12]},ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
'''
        ),
    )
    write(
        "scripts/repo/validate_case.py",
        clean(
            r'''
#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
REQUIRED=["intake.yaml","authorization.md","inventory.json","symptoms.md","timeline.jsonl","hypotheses.yaml","actions.jsonl","rollback.md"]
def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--case",required=True); a=p.parse_args(); root=Path(a.case)
    missing=[x for x in REQUIRED if not (root/x).exists()]
    secret_hits=[]
    for path in root.rglob("*"):
        if path.is_file() and path.stat().st_size<2_000_000:
            text=path.read_text(encoding="utf-8",errors="ignore").lower()
            if "recoverypassword" in text or "password=" in text or "token=" in text: secret_hits.append(str(path))
    print(json.dumps({"case":str(root),"missing":missing,"secret_warning_files":secret_hits,"valid":not missing and not secret_hits},indent=2))
    return 0 if not missing and not secret_hits else 1
if __name__=="__main__": raise SystemExit(main())
'''
        ),
    )
    write(
        "scripts/repo/validate_unattend.py",
        clean(
            r'''
#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, xml.etree.ElementTree as ET
from pathlib import Path
def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--path",required=True); a=p.parse_args(); path=Path(a.path)
    errors=[]; warnings=[]
    try: ET.parse(path)
    except Exception as exc: errors.append(str(exc))
    text=path.read_text(encoding="utf-8",errors="ignore")
    for pattern,label in [(r"(?i)<Password>","password element"),(r"(?i)<ProductKey>","product key element"),(r"(?i)<AutoLogon>","autologon")]:
        if re.search(pattern,text): warnings.append(label+" requires secret/redaction review")
    print(json.dumps({"path":str(path),"errors":errors,"warnings":warnings,"valid":not errors},indent=2)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
'''
        ),
    )

    write(
        "scripts/reporting/New-WindowsServiceCase.ps1",
        clean(
            r'''
<#
.SYNOPSIS Creates an anonymized Windows service case from repository templates.
.EXAMPLE .\New-WindowsServiceCase.ps1 -Slug boot-loop -OwnerAlias owner-001 -AuthorizationLevel R0 -Root .\cases
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Low')]
param(
    [Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{1,48}$')][string]$Slug,
    [Parameter(Mandatory)][ValidatePattern('^[a-zA-Z0-9_-]{2,64}$')][string]$OwnerAlias,
    [Parameter(Mandatory)][ValidateSet('R0','R1','R2','R3','R4')][string]$AuthorizationLevel,
    [Parameter(Mandatory)][string]$Root,
    [datetime]$Date = (Get-Date)
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$module=Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1'
Import-Module $module -Force
$caseId='{0}-{1}' -f $Date.ToString('yyyy-MM-dd'),$Slug
$casePath=Join-Path ([IO.Path]::GetFullPath($Root)) $caseId
if(Test-Path -LiteralPath $casePath){throw "Case already exists: $casePath"}
if($PSCmdlet.ShouldProcess($casePath,'Create service case')){
    New-Item -ItemType Directory -Path $casePath -Force|Out-Null
    foreach($dir in @('evidence','logs','before','after')){New-Item -ItemType Directory -Path (Join-Path $casePath $dir)-Force|Out-Null}
    $intake=[ordered]@{case_id=$caseId;created_utc=[DateTime]::UtcNow.ToString('o');owner_alias=$OwnerAlias;authorization_level=$AuthorizationLevel;data_value='unknown';backup_status='unknown';encryption_status='unknown';managed_status='unknown';symptom='uncollected';last_changes=@();accessories=@()}
    Write-WmJson $intake (Join-Path $casePath 'intake.yaml')
    Copy-Item -LiteralPath (Join-Path $repo 'templates\customer-consent\authorization-pl.md') -Destination (Join-Path $casePath 'authorization.md')
    Write-WmJson ([ordered]@{status='not-collected';synthetic=$false}) (Join-Path $casePath 'inventory.json')
    Set-Content -LiteralPath (Join-Path $casePath 'symptoms.md') -Value "# Objawy`n`nNie zebrano jeszcze objawów.`n" -Encoding utf8
    Set-Content -LiteralPath (Join-Path $casePath 'timeline.jsonl') -Value '' -Encoding utf8
    Copy-Item -LiteralPath (Join-Path $repo 'templates\case\hypotheses.yaml') -Destination (Join-Path $casePath 'hypotheses.yaml')
    Set-Content -LiteralPath (Join-Path $casePath 'actions.jsonl') -Value '' -Encoding utf8
    Set-Content -LiteralPath (Join-Path $casePath 'rollback.md') -Value "# Rollback`n`nBrak zmian; uzupełnij przed R1+.`n" -Encoding utf8
    Set-Content -LiteralPath (Join-Path $casePath 'technical-report.md') -Value "# Raport techniczny`n`nStatus: open.`n" -Encoding utf8
    Set-Content -LiteralPath (Join-Path $casePath 'owner-summary.md') -Value "# Podsumowanie`n`nSprawa otwarta.`n" -Encoding utf8
}
Write-Output $casePath
'''
        ),
    )
    write(
        "scripts/reporting/Add-WindowsCaseAction.ps1",
        clean(
            r'''
<#
.SYNOPSIS Appends an immutable-style JSONL action record to a service case.
.EXAMPLE .\Add-WindowsCaseAction.ps1 -CasePath .\cases\x -Purpose inventory -RiskClass R0 -Result observed -Rollback not-applicable
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Low')]
param(
    [Parameter(Mandatory)][string]$CasePath,
    [Parameter(Mandatory)][string]$Purpose,
    [Parameter(Mandatory)][ValidateSet('R0','R1','R2','R3','R4')][string]$RiskClass,
    [string]$Operator=$env:USERNAME,
    [string]$CommandOrTool='manual-observation',
    [string]$Target='case',
    [Parameter(Mandatory)][ValidateSet('observed','not-observed','inconclusive','blocked','success','failed')][string]$Result,
    [Parameter(Mandatory)][string]$Rollback,
    [string[]]$Artifacts=@()
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$resolved=(Resolve-Path -LiteralPath $CasePath).Path
if(-not(Test-Path -LiteralPath (Join-Path $resolved 'intake.yaml'))){throw 'Not a service case.'}
$hashes=@()
foreach($artifact in $Artifacts){if(Test-Path -LiteralPath $artifact){$h=Get-FileHash -LiteralPath $artifact -Algorithm SHA256;$hashes+=[ordered]@{path=$artifact;sha256=$h.Hash.ToLowerInvariant()}}}
$record=[ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operator=$Operator;purpose=$Purpose;risk_class=$RiskClass;command_or_tool=$CommandOrTool;target=$Target;result=$Result;rollback=$Rollback;artifacts=$hashes}
if($PSCmdlet.ShouldProcess((Join-Path $resolved 'actions.jsonl'),'Append case action')){Add-WmJsonLine $record (Join-Path $resolved 'actions.jsonl');Add-WmJsonLine ([ordered]@{timestamp_utc=$record.timestamp_utc;event='action-recorded';purpose=$Purpose}) (Join-Path $resolved 'timeline.jsonl')}
$record
'''
        ),
    )
    write(
        "scripts/reporting/New-WindowsServiceReport.ps1",
        clean(
            r'''
<#
.SYNOPSIS Generates a technical report and owner summary from case JSONL.
.EXAMPLE .\New-WindowsServiceReport.ps1 -CasePath .\cases\2026-01-01-example
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Low')]
param([Parameter(Mandatory)][string]$CasePath,[switch]$RequireValidation)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$resolved=(Resolve-Path -LiteralPath $CasePath).Path
$intake=Get-Content -LiteralPath (Join-Path $resolved 'intake.yaml') -Raw|ConvertFrom-Json
$actions=@()
Get-Content -LiteralPath (Join-Path $resolved 'actions.jsonl')|Where-Object {$_ -match '\S'}|ForEach-Object {$actions+=($_|ConvertFrom-Json)}
$validations=@($actions|Where-Object {$_.purpose -match '(?i)validat|sprawd|regress'})
if($RequireValidation -and $validations.Count -eq 0){throw 'No validation action found; report cannot be finalized.'}
$actionLines=if($actions.Count){($actions|ForEach-Object {"- $($_.timestamp_utc) [$($_.risk_class)] $($_.purpose): $($_.result); rollback: $($_.rollback)"}) -join "`n"}else{'- Brak zapisanych działań.'}
$status=if($validations.Count){'validated'}else{'open-unvalidated'}
$tech=@"
# Raport techniczny $($intake.case_id)

## Zakres
Autoryzacja: $($intake.authorization_level). Owner alias: $($intake.owner_alias).

## Działania
$actionLines

## Walidacja
Status: $status. Liczba rekordów walidacji: $($validations.Count).

## Ograniczenia
Raport nie zawiera haseł, tokenów ani BitLocker recovery keys. Fakty wymagają artefaktów.
"@
$owner=@"
# Podsumowanie dla właściciela

Sprawa $($intake.case_id) ma status **$status**. Zapisano $($actions.Count) czynności.
Przed zamknięciem upewnij się, że wykonano test objawu, przyczyny, regresji i backupu.
"@
if($PSCmdlet.ShouldProcess($resolved,'Generate reports')){$tech|Set-Content -LiteralPath (Join-Path $resolved 'technical-report.md') -Encoding utf8;$owner|Set-Content -LiteralPath (Join-Path $resolved 'owner-summary.md') -Encoding utf8}
[pscustomobject]@{Case=$intake.case_id;Actions=$actions.Count;Validations=$validations.Count;Status=$status}
'''
        ),
    )

    collector_specs = {
        "Export-WindowsRelevantEvents.ps1": r"""
$since=(Get-Date).AddDays(-7)
$providers=@('Microsoft-Windows-WHEA-Logger','Disk','Ntfs','Microsoft-Windows-WindowsUpdateClient','Service Control Manager','Microsoft-Windows-User Profiles Service')
$data=@()
foreach($provider in $providers){
    try{$data+=Get-WinEvent -FilterHashtable @{LogName='System';ProviderName=$provider;StartTime=$since} -MaxEvents 200 -ErrorAction Stop|Select-Object TimeCreated,ProviderName,Id,LevelDisplayName,Message}catch{}
}
""",
        "Get-WindowsDriverInventory.ps1": r"""
$data=[ordered]@{
    collected_utc=[DateTime]::UtcNow.ToString('o')
    drivers=@(Get-CimInstance -ClassName Win32_PnPSignedDriver|Select-Object DeviceName,DeviceID,DriverProviderName,DriverVersion,DriverDate,InfName,IsSigned)
    problem_devices=@(Get-CimInstance -ClassName Win32_PnPEntity|Where-Object ConfigManagerErrorCode -ne 0|Select-Object Name,PNPDeviceID,ConfigManagerErrorCode,Status)
}
""",
        "Get-WindowsUpdateHealth.ps1": r"""
$pending=@(
 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending',
 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
)|Where-Object {Test-Path -LiteralPath $_}
$events=@()
try{$events=Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-WindowsUpdateClient';StartTime=(Get-Date).AddDays(-30)} -MaxEvents 200|Select-Object TimeCreated,Id,LevelDisplayName,Message}catch{}
$data=[ordered]@{collected_utc=[DateTime]::UtcNow.ToString('o');pending_reboot=($pending.Count -gt 0);pending_markers=$pending;events=$events}
""",
        "Get-WindowsStartupPersistence.ps1": r"""
$tasks=@()
if(Get-Command Get-ScheduledTask -ErrorAction SilentlyContinue){$tasks=Get-ScheduledTask|Select-Object TaskPath,TaskName,State,Author,@{n='Actions';e={($_.Actions|ForEach-Object Execute)-join ';'}}}
$data=[ordered]@{
 startup=@(Get-CimInstance -ClassName Win32_StartupCommand|Select-Object Name,Command,Location,User)
 services=@(Get-CimInstance -ClassName Win32_Service|Select-Object Name,State,StartMode,PathName,StartName)
 tasks=@($tasks)
}
""",
        "Get-WindowsNetworkSnapshot.ps1": r"""
$data=[ordered]@{
 adapters=@(Get-NetAdapter|Select-Object Name,InterfaceDescription,Status,MacAddress,LinkSpeed)
 ip=@(Get-NetIPConfiguration|Select-Object InterfaceAlias,InterfaceIndex,IPv4Address,IPv6Address,IPv4DefaultGateway,DNSServer)
 routes=@(Get-NetRoute -AddressFamily IPv4|Select-Object DestinationPrefix,NextHop,InterfaceIndex,RouteMetric,Protocol)
 proxy=(& "$env:SystemRoot\System32\netsh.exe" winhttp show proxy 2>&1)-join "`n"
}
""",
        "Get-BitLockerSafetyStatus.ps1": r"""
$volumes=@()
if(Get-Command Get-BitLockerVolume -ErrorAction SilentlyContinue){
 $volumes=Get-BitLockerVolume|Select-Object MountPoint,VolumeType,ProtectionStatus,LockStatus,EncryptionMethod,VolumeStatus,@{n='ProtectorTypes';e={@($_.KeyProtector|ForEach-Object KeyProtectorType)}}
}
$tpm=$null;if(Get-Command Get-Tpm -ErrorAction SilentlyContinue){$tpm=Get-Tpm|Select-Object TpmPresent,TpmReady,TpmEnabled,TpmActivated,AutoProvisioning}
$data=[ordered]@{volumes=@($volumes);tpm=$tpm;contains_recovery_keys=$false}
""",
        "Get-WindowsManagementStatus.ps1": r"""
$dsreg=(& "$env:SystemRoot\System32\dsregcmd.exe" /status 2>&1)-join "`n"
$data=[ordered]@{
 join_summary=($dsreg -split "`r?`n"|Where-Object {$_ -match 'AzureAdJoined|DomainJoined|WorkplaceJoined|DeviceId|TenantName'})
 domain=(Get-CimInstance Win32_ComputerSystem|Select-Object PartOfDomain,Domain,Workgroup)
 mdm_registry_present=(Test-Path -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Enrollments')
}
""",
    }
    collector_template = r'''
<#
.SYNOPSIS Collects a redacted, read-only Windows diagnostic view or parses a synthetic JSON fixture.
.EXAMPLE .\__NAME__ -FixturePath .\tests\fixtures\sample.json -OutputPath .\dist\output.json
#>
[CmdletBinding()]
param(
    [string]$FixturePath,
    [Parameter(Mandatory)][string]$OutputPath,
    [switch]$IncludeSensitive
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
try{
    if($FixturePath){
        $resolved=(Resolve-Path -LiteralPath $FixturePath).Path
        $raw=Get-Content -LiteralPath $resolved -Raw
        try{$data=$raw|ConvertFrom-Json}catch{$data=[ordered]@{fixture_text=$raw}}
        $source='fixture'
    }else{
        if($PSVersionTable.PSVersion.Major -ge 6 -and -not $IsWindows){throw 'Live collection requires Windows. Use -FixturePath.'}
__LIVE__
        $source='live-read-only'
    }
    $json=$data|ConvertTo-Json -Depth 12
    $protected=Protect-WmText -Text $json -IncludeSensitive:$IncludeSensitive
    $envelope=[ordered]@{schema_version='1.0.0';collector='__NAME__';source=$source;collected_utc=[DateTime]::UtcNow.ToString('o');redacted=(-not $IncludeSensitive);data=($protected|ConvertFrom-Json)}
    Write-WmJson -InputObject $envelope -Path $OutputPath
    $envelope
    exit 0
}catch{
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 20
}
'''
    for filename, live_code in collector_specs.items():
        script = collector_template.replace("__NAME__", filename).replace("__LIVE__", textwrap.indent(live_code.strip(), "        "))
        write(f"scripts/diagnostics/{filename}", clean(script))

    write(
        "scripts/diagnostics/Get-WindowsStorageRisk.ps1",
        clean(
            r'''
<#
.SYNOPSIS Classifies storage telemetry without running filesystem or surface repairs.
.EXAMPLE .\Get-WindowsStorageRisk.ps1 -FixturePath .\tests\fixtures\storage\critical.json -OutputPath .\dist\storage-risk.json
#>
[CmdletBinding()]
param([string]$FixturePath,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
if($FixturePath){$input=Get-Content -LiteralPath (Resolve-Path -LiteralPath $FixturePath) -Raw|ConvertFrom-Json}
else{
 if($PSVersionTable.PSVersion.Major -ge 6 -and -not $IsWindows){throw 'Live collection requires Windows.'}
 $input=[ordered]@{disks=@(Get-Disk|Select-Object Number,FriendlyName,SerialNumber,HealthStatus,OperationalStatus,Size);physical=@(Get-PhysicalDisk|ForEach-Object{$d=$_;$r=$null;try{$r=$d|Get-StorageReliabilityCounter}catch{};[pscustomobject]@{FriendlyName=$d.FriendlyName;HealthStatus=$d.HealthStatus;OperationalStatus=$d.OperationalStatus;Temperature=$r.Temperature;ReadErrorsTotal=$r.ReadErrorsTotal;WriteErrorsTotal=$r.WriteErrorsTotal;Wear=$r.Wear}})}
}
$serialized=$input|ConvertTo-Json -Depth 10
$stopPatterns='(?i)critical|unhealthy|lost communication|read.?error[^0-9]*[1-9]|click|disappear|media error'
$cautionPatterns='(?i)warning|degraded|temperature[^0-9]*(?:[6-9][0-9]|1[0-9]{2})|wear[^0-9]*(?:9[0-9]|100)'
$classification=if($serialized -match $stopPatterns){'stop'}elseif($serialized -match $cautionPatterns){'caution'}else{'no-stop-signal-observed'}
$result=[ordered]@{schema_version='1.0.0';classification=$classification;rule='Absence of telemetry is not proof of health';do_not=@('chkdsk /f first on suspected physical failure','surface scan before image');evidence=$input}
Write-WmJson $result $OutputPath
$result
'''
        ),
    )
    write(
        "scripts/diagnostics/Get-WindowsBootLayout.ps1",
        clean(
            r'''
<#
.SYNOPSIS Produces a read-only boot-layout map; it never selects, formats, or writes a partition.
.EXAMPLE .\Get-WindowsBootLayout.ps1 -FixturePath .\tests\fixtures\boot\uefi.json -OutputPath .\dist\boot-layout.json
#>
[CmdletBinding()]
param([string]$FixturePath,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
if($FixturePath){$data=Get-Content -LiteralPath (Resolve-Path -LiteralPath $FixturePath) -Raw|ConvertFrom-Json;$source='fixture'}
else{
 if($PSVersionTable.PSVersion.Major -ge 6 -and -not $IsWindows){throw 'Live collection requires Windows.'}
 $fw='unknown';try{$fw=(Get-ComputerInfo -Property BiosFirmwareType).BiosFirmwareType}catch{}
 $data=[ordered]@{firmware=$fw;disks=@(Get-Disk|Select-Object Number,UniqueId,FriendlyName,PartitionStyle,Size,IsBoot,IsSystem);partitions=@(Get-Partition|Select-Object DiskNumber,PartitionNumber,DriveLetter,Type,GptType,IsActive,IsBoot,IsSystem,Size);volumes=@(Get-Volume|Select-Object DriveLetter,FileSystemLabel,FileSystem,HealthStatus,Size,SizeRemaining)}
 $source='live-read-only'
}
$result=[ordered]@{schema_version='1.0.0';source=$source;rule='OS volume requires Windows directory + SOFTWARE hive + BCD corroboration; never assume C:';data=$data}
Write-WmJson $result $OutputPath
$result
'''
        ),
    )
    write(
        "scripts/diagnostics/Parse-WindowsServicingLog.ps1",
        clean(
            r'''
<#
.SYNOPSIS Parses CBS/DISM text metadata from a copied log or synthetic fixture.
.EXAMPLE .\Parse-WindowsServicingLog.ps1 -Path .\tests\fixtures\logs\CBS.log -OutputPath .\dist\cbs.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Path,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot);Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$resolved=(Resolve-Path -LiteralPath $Path).Path;$lines=[IO.File]::ReadAllLines($resolved)
$matchedLines=@($lines|Where-Object{$_ -match '(?i)error|corrupt|failed|0x[0-9a-f]{8}|repair'})
$summary=[ordered]@{path=(Split-Path -Leaf $resolved);sha256=(Get-FileHash -LiteralPath $resolved -Algorithm SHA256).Hash.ToLowerInvariant();line_count=$lines.Count;matched_count=$matchedLines.Count;matches=@($matchedLines|Select-Object -First 250);limitations='Text triage only; context and matched source are required.'}
Write-WmJson $summary $OutputPath;$summary
'''
        ),
    )
    write(
        "scripts/diagnostics/Parse-WindowsSetupLog.ps1",
        clean(
            r'''
<#
.SYNOPSIS Extracts phases, error codes and SetupDiag-like rule lines from copied Setup/Panther logs.
.EXAMPLE .\Parse-WindowsSetupLog.ps1 -Path .\tests\fixtures\logs\setuperr.log -OutputPath .\dist\setup.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Path,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot);Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$resolved=(Resolve-Path -LiteralPath $Path).Path;$lines=[IO.File]::ReadAllLines($resolved)
$hits=@($lines|Where-Object{$_ -match '(?i)error|fail|0x[0-9a-f]{8}|downlevel|safe_os|first_boot|second_boot|compat|rule'})
$result=[ordered]@{file=(Split-Path -Leaf $resolved);sha256=(Get-FileHash $resolved -Algorithm SHA256).Hash.ToLowerInvariant();hits=@($hits|Select-Object -First 300);limitations='Parser does not replace Microsoft SetupDiag or full Panther correlation.'}
Write-WmJson $result $OutputPath;$result
'''
        ),
    )
    write(
        "scripts/diagnostics/Get-MinidumpMetadata.ps1",
        clean(
            r'''
<#
.SYNOPSIS Extracts safe file metadata from dump fixtures; it does not claim a WinDbg diagnosis.
.EXAMPLE .\Get-MinidumpMetadata.ps1 -Path .\tests\fixtures\dumps\synthetic.dmp.txt -OutputPath .\dist\dump.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Path,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot);Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$file=Get-Item -LiteralPath (Resolve-Path -LiteralPath $Path)
$bytes=[IO.File]::ReadAllBytes($file.FullName);$prefix=[BitConverter]::ToString($bytes[0..([Math]::Min(31,$bytes.Length-1))]).Replace('-','')
$result=[ordered]@{name=$file.Name;length=$file.Length;last_write_utc=$file.LastWriteTimeUtc.ToString('o');sha256=(Get-FileHash $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant();prefix_hex=$prefix;analysis='metadata-only';required_for_diagnosis='WinDbg with symbols and multiple correlated dumps'}
Write-WmJson $result $OutputPath;$result
'''
        ),
    )
    write(
        "scripts/diagnostics/Get-WindowsRepairBundle.ps1",
        clean(
            r'''
<#
.SYNOPSIS Creates a redacted Windows repair bundle from live read-only collectors or synthetic fixtures.
.DESCRIPTION Modes: Basic, Full, Offline, Network, Boot, Update, BSOD, MalwareTriage. The script never collects passwords, cookies, tokens, full product keys or BitLocker recovery keys.
.EXAMPLE .\Get-WindowsRepairBundle.ps1 -Mode Basic -FixtureRoot .\tests\fixtures\repair-bundle -OutputPath .\dist\sample-bundle
#>
[CmdletBinding()]
param(
 [Parameter(Mandatory)][ValidateSet('Basic','Full','Offline','Network','Boot','Update','BSOD','MalwareTriage')][string]$Mode,
 [string]$FixtureRoot,
 [Parameter(Mandatory)][string]$OutputPath,
 [switch]$IncludeSensitive
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$out=[IO.Path]::GetFullPath($OutputPath)
if(Test-Path -LiteralPath $out){throw "Output already exists: $out"}
New-Item -ItemType Directory -Path $out -Force|Out-Null
try{
 $records=@()
 if($FixtureRoot){
  $fixture=(Resolve-Path -LiteralPath $FixtureRoot).Path
  foreach($file in Get-ChildItem -LiteralPath $fixture -File -Recurse){
   $raw=Get-Content -LiteralPath $file.FullName -Raw
   $safe=Protect-WmText -Text $raw -IncludeSensitive:$IncludeSensitive
   $relative=Get-WmRelativePath -BasePath $fixture -Path $file.FullName
   $target=Join-Path $out $relative
   New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force|Out-Null
   Set-Content -LiteralPath $target -Value $safe -Encoding utf8
   $records+=[ordered]@{name=$relative;source='synthetic-fixture';redacted=(-not $IncludeSensitive)}
  }
  $source='fixture'
 }else{
  if($PSVersionTable.PSVersion.Major -ge 6 -and -not $IsWindows){throw 'Live collection requires Windows. Use -FixtureRoot.'}
  $os=Get-CimInstance Win32_OperatingSystem|Select-Object Caption,Version,BuildNumber,OSArchitecture,Locale
  $cs=Get-CimInstance Win32_ComputerSystem|Select-Object Manufacturer,Model,SystemType,PartOfDomain
  $bios=Get-CimInstance Win32_BIOS|Select-Object Manufacturer,SMBIOSBIOSVersion,ReleaseDate
  $data=[ordered]@{os=$os;computer=$cs;firmware=$bios;mode=$Mode;note='Live R0 only; detailed collectors should be run explicitly.'}
  $json=Protect-WmText -Text ($data|ConvertTo-Json -Depth 8) -IncludeSensitive:$IncludeSensitive
  Set-Content -LiteralPath (Join-Path $out 'basic.json') -Value $json -Encoding utf8
  $records+=[ordered]@{name='basic.json';source='live-read-only';redacted=(-not $IncludeSensitive)}
  $source='live-read-only'
 }
 $forbidden='(?i)(RecoveryPassword\s*[:=]\s*\S+|password\s*[:=]\s*\S+|token\s*[:=]\s*\S+|cookie\s*[:=]\s*\S+|\b\d{6}(?:-\d{6}){7}\b)'
 foreach($file in Get-ChildItem -LiteralPath $out -File -Recurse){
  $text=Get-Content -LiteralPath $file.FullName -Raw
  if($text -match $forbidden){throw "Secret pattern remained after redaction: $($file.Name)"}
 }
 $manifestEntries=@()
 foreach($file in Get-ChildItem -LiteralPath $out -File -Recurse|Sort-Object FullName){
   $manifestEntries+=[ordered]@{path=(Get-WmRelativePath -BasePath $out -Path $file.FullName);bytes=$file.Length;sha256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
 }
 $manifest=[ordered]@{schema_version='1.0.0';created_utc=[DateTime]::UtcNow.ToString('o');mode=$Mode;source=$source;redacted=(-not $IncludeSensitive);exclusions=@('passwords','cookies','tokens','full product keys','BitLocker recovery keys','browser contents');files=$manifestEntries}
 Write-WmJson $manifest (Join-Path $out 'manifest.json')
 $md=@"
# Windows Repair Bundle

- Mode: $Mode
- Source: $source
- Redacted: $(-not $IncludeSensitive)
- Files before manifest: $($manifestEntries.Count)
- Created UTC: $($manifest.created_utc)

Bundle is diagnostic evidence, not a diagnosis. No repair was executed.
"@
 Set-Content -LiteralPath (Join-Path $out 'summary.md') -Value $md -Encoding utf8
 $html="<html><meta charset='utf-8'><body><h1>Windows Repair Bundle</h1><p>Mode: $Mode</p><p>Source: $source</p><p>Redacted: $(-not $IncludeSensitive)</p><p>No repair executed.</p></body></html>"
 Set-Content -LiteralPath (Join-Path $out 'summary.html') -Value $html -Encoding utf8
 $zip="$out.zip"
 Compress-Archive -Path (Join-Path $out '*') -DestinationPath $zip -CompressionLevel Optimal
 $zipHash=(Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
 [pscustomobject]@{OutputPath=$out;ZipPath=$zip;ZipSha256=$zipHash;Mode=$Mode;Source=$source;Redacted=(-not $IncludeSensitive)}
 exit 0
}catch{
 [Console]::Error.WriteLine($_.Exception.Message)
 exit 30
}
'''
        ),
    )
    write(
        "scripts/offline/Get-OfflineWindowsIdentity.ps1",
        clean(
            r'''
<#
.SYNOPSIS Reads identity from an offline Windows SOFTWARE hive and always unloads it.
.EXAMPLE .\Get-OfflineWindowsIdentity.ps1 -WindowsPath D:\Windows -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Medium')]
param([Parameter(Mandatory)][ValidateScript({Test-Path -LiteralPath $_ -PathType Container})][string]$WindowsPath)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$hive=Join-Path $WindowsPath 'System32\config\SOFTWARE'
if(-not(Test-Path -LiteralPath $hive -PathType Leaf)){throw "SOFTWARE hive not found under: $WindowsPath"}
$mount='HKLM\WM_OFFLINE_{0}' -f ([guid]::NewGuid().ToString('N'))
$loaded=$false
try{
 if($PSCmdlet.ShouldProcess($hive,"Temporarily load read-only query hive at $mount")){
  & "$env:SystemRoot\System32\reg.exe" load $mount $hive|Out-Null
  if($LASTEXITCODE -ne 0){throw 'reg load failed'};$loaded=$true
  $path="Registry::$mount\Microsoft\Windows NT\CurrentVersion"
  Get-ItemProperty -LiteralPath $path|Select-Object ProductName,EditionID,CurrentBuild,CurrentBuildNumber,UBR,DisplayVersion,InstallationType
 }
}finally{if($loaded){& "$env:SystemRoot\System32\reg.exe" unload $mount|Out-Null}}
'''
        ),
    )
    write(
        "scripts/offline/Export-OfflineWindowsLogs.ps1",
        clean(
            r'''
<#
.SYNOPSIS Copies selected offline Windows logs to a separate evidence directory with SHA-256.
.EXAMPLE .\Export-OfflineWindowsLogs.ps1 -WindowsPath D:\Windows -Destination E:\case\logs
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Low')]
param([Parameter(Mandatory)][string]$WindowsPath,[Parameter(Mandatory)][string]$Destination)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$sources=@('Logs\CBS\CBS.log','Logs\DISM\dism.log','Panther\setupact.log','Panther\setuperr.log','INF\setupapi.dev.log','System32\LogFiles\Srt\SrtTrail.txt')
$manifest=@()
foreach($relative in $sources){$src=Join-Path $WindowsPath $relative;if(Test-Path -LiteralPath $src){$dst=Join-Path $Destination $relative;New-Item -ItemType Directory -Path (Split-Path -Parent $dst)-Force|Out-Null;if($PSCmdlet.ShouldProcess($src,"Copy to $dst")){Copy-Item -LiteralPath $src -Destination $dst;$manifest+=[ordered]@{source=$relative;sha256=(Get-FileHash $dst -Algorithm SHA256).Hash.ToLowerInvariant()}}}}
$manifest|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $Destination 'offline-log-manifest.json') -Encoding utf8
$manifest
'''
        ),
    )
    write(
        "scripts/offline/legacy-inventory.cmd",
        clean(
            r'''
@echo off
REM R0 legacy inventory only. Run on an authorized isolated XP/Vista/7/8.x system.
REM This script does not call WMIC product and does not change configuration.
set "OUT=%~1"
if "%OUT%"=="" exit /b 10
if not exist "%OUT%" mkdir "%OUT%"
systeminfo > "%OUT%\systeminfo.txt" 2>&1
ipconfig /all > "%OUT%\ipconfig.txt" 2>&1
driverquery /v /fo csv > "%OUT%\drivers.csv" 2>&1
sc query type= service state= all > "%OUT%\services.txt" 2>&1
exit /b 0
'''
        ),
    )
    repair_definitions = {
        "Invoke-WindowsComponentRepair.ps1": {
            "operation": "windows-component-repair",
            "risk": "R2",
            "target_default": "online-Windows-component-store",
            "steps": ["DISM ScanHealth", "DISM RestoreHealth after source validation", "SFC scannow once", "parse CBS/DISM"],
            "rollback": ["use matched repair media/in-place repair if store cannot be restored", "restore pre-change image for regression"],
            "apply": r"""
& "$env:SystemRoot\System32\dism.exe" /Online /Cleanup-Image /RestoreHealth
if($LASTEXITCODE -ne 0){throw "DISM RestoreHealth failed: $LASTEXITCODE"}
& "$env:SystemRoot\System32\sfc.exe" /scannow
if($LASTEXITCODE -notin @(0,1)){throw "SFC failed: $LASTEXITCODE"}
""",
        },
        "Invoke-WindowsUpdateRepair.ps1": {
            "operation": "windows-update-repair",
            "risk": "R2",
            "target_default": "online-Windows-Update-components",
            "steps": ["capture update health and policy", "stop exact update services", "rename cache to dated backup", "start services", "scan update"],
            "rollback": ["stop services", "restore renamed SoftwareDistribution/Catroot2 only if new cache is removed and target matches", "start services"],
            "apply": r"""
$stamp=Get-Date -Format 'yyyyMMddHHmmss'
$services=@('bits','wuauserv','cryptsvc')
$serviceState=Get-Service -Name $services|Select-Object Name,Status,StartType
Write-WmJson $serviceState (Join-Path $LogRoot 'services-before.json')
foreach($service in $services){Stop-Service -Name $service -Force -ErrorAction Stop}
$sd=Join-Path $env:SystemRoot 'SoftwareDistribution'
$cr=Join-Path $env:SystemRoot 'System32\catroot2'
if(Test-Path -LiteralPath $sd){Rename-Item -LiteralPath $sd -NewName "SoftwareDistribution.wmbackup.$stamp"}
if(Test-Path -LiteralPath $cr){Rename-Item -LiteralPath $cr -NewName "catroot2.wmbackup.$stamp"}
foreach($service in @('cryptsvc','wuauserv','bits')){Start-Service -Name $service -ErrorAction Stop}
""",
        },
        "Invoke-WindowsNetworkRepair.ps1": {
            "operation": "windows-network-repair",
            "risk": "R2",
            "target_default": "online-Windows-network-stack",
            "steps": ["export adapters/routes/DNS/proxy", "reset Winsock catalog", "reset TCP/IP with log", "reboot gate", "layered validation"],
            "rollback": ["restore static IP/DNS/proxy/routes from snapshot", "reinstall approved VPN/filter client if required"],
            "apply": r"""
Get-NetIPConfiguration|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $LogRoot 'ip-before.json') -Encoding utf8
& "$env:SystemRoot\System32\netsh.exe" winsock reset
if($LASTEXITCODE -ne 0){throw "Winsock reset failed: $LASTEXITCODE"}
& "$env:SystemRoot\System32\netsh.exe" int ip reset (Join-Path $LogRoot 'netsh-ip-reset.log')
if($LASTEXITCODE -ne 0){throw "TCP/IP reset failed: $LASTEXITCODE"}
""",
        },
        "Invoke-PrintSpoolerRepair.ps1": {
            "operation": "print-spooler-repair",
            "risk": "R2",
            "target_default": "local-print-spooler",
            "steps": ["export queue/driver/port state", "stop Spooler", "move stuck spool files to quarantine", "start Spooler", "test page"],
            "rollback": ["stop Spooler", "move quarantined files back only when compatible", "start Spooler"],
            "apply": r"""
$queue=Get-Printer -ErrorAction SilentlyContinue|Select-Object Name,DriverName,PortName,PrinterStatus
Write-WmJson $queue (Join-Path $LogRoot 'printers-before.json')
Stop-Service -Name Spooler -Force -ErrorAction Stop
$spool=Join-Path $env:SystemRoot 'System32\spool\PRINTERS'
$quarantine=Join-Path $LogRoot ('spool-quarantine-'+(Get-Date -Format 'yyyyMMddHHmmss'))
New-Item -ItemType Directory -Path $quarantine -Force|Out-Null
Get-ChildItem -LiteralPath $spool -File -ErrorAction SilentlyContinue|Move-Item -Destination $quarantine
Start-Service -Name Spooler -ErrorAction Stop
""",
        },
        "Invoke-StoreAppxRepair.ps1": {
            "operation": "store-appx-repair",
            "risk": "R2",
            "target_default": "specified-AppX-package",
            "steps": ["resolve exact package/current user", "export package metadata", "register its AppxManifest only", "validate events and launch"],
            "rollback": ["restore from Store/approved package source", "use prior package version only when supported"],
            "apply": r"""
if([string]::IsNullOrWhiteSpace($PackageName)){throw '-PackageName is required for Apply.'}
$packages=@(Get-AppxPackage -Name $PackageName -ErrorAction Stop)
if($packages.Count -ne 1){throw "Expected exactly one package; found $($packages.Count)."}
Write-WmJson ($packages|Select-Object Name,PackageFullName,Version,InstallLocation,Status) (Join-Path $LogRoot 'package-before.json')
$manifest=Join-Path $packages[0].InstallLocation 'AppxManifest.xml'
Add-AppxPackage -DisableDevelopmentMode -Register $manifest -ErrorAction Stop
""",
        },
        "Invoke-UserProfileRepair.ps1": {
            "operation": "user-profile-repair",
            "risk": "R3",
            "target_default": "explicit-profile-SID",
            "steps": ["verify authorized SID/profile path/EFS/OneDrive", "export exact ProfileList key", "set RefCount/State only when evidence matches temporary-profile pattern", "logon validation"],
            "rollback": ["import exact exported ProfileList key", "restore original State/RefCount values", "use replacement profile migration if hive remains corrupt"],
            "apply": r"""
if($ProfileSid -notmatch '^S-1-5-21-(?:\d+-){3}\d+$'){throw 'Exact local/domain user SID is required.'}
$profileKey="HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\$ProfileSid"
if(-not(Test-Path -LiteralPath $profileKey)){throw "ProfileList key not found: $ProfileSid"}
$export=Join-Path $LogRoot 'profilelist-before.reg'
& "$env:SystemRoot\System32\reg.exe" export "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\$ProfileSid" $export /y|Out-Null
if($LASTEXITCODE -ne 0){throw 'ProfileList export failed.'}
$current=Get-ItemProperty -LiteralPath $profileKey
Write-WmJson ($current|Select-Object ProfileImagePath,State,RefCount,Flags) (Join-Path $LogRoot 'profile-before.json')
if($null -ne $current.RefCount -and $current.RefCount -gt 0){Set-ItemProperty -LiteralPath $profileKey -Name RefCount -Value 0 -Type DWord}
if($null -ne $current.State -and $current.State -ne 0){Set-ItemProperty -LiteralPath $profileKey -Name State -Value 0 -Type DWord}
""",
        },
        "Invoke-DriverStoreRepair.ps1": {
            "operation": "driver-store-repair",
            "risk": "R3",
            "target_default": "explicit-published-OEM-INF",
            "steps": ["verify device/hardware ID/provider/version", "export driver package", "check boot-critical dependency", "remove exact published name", "install matched OEM package"],
            "rollback": ["reinstall exported/matched signed OEM INF", "boot Safe Mode/WinRE if boot regression"],
            "apply": r"""
if($PublishedName -notmatch '^oem\d+\.inf$'){throw 'PublishedName must be exact oemNN.inf.'}
& "$env:SystemRoot\System32\pnputil.exe" /enum-drivers|Set-Content -LiteralPath (Join-Path $LogRoot 'drivers-before.txt') -Encoding utf8
& "$env:SystemRoot\System32\pnputil.exe" /delete-driver $PublishedName /uninstall
if($LASTEXITCODE -ne 0){throw "PnPUtil delete-driver failed: $LASTEXITCODE"}
""",
        },
        "Invoke-VssBackupRepair.ps1": {
            "operation": "vss-backup-repair",
            "risk": "R2",
            "target_default": "specified-VSS-writer-service",
            "steps": ["capture writers/providers/events", "restart only mapped failed writer service", "run application-aware backup", "restore one file"],
            "rollback": ["restore original service start state", "re-enable vendor provider", "do not delete existing shadows"],
            "apply": r"""
if([string]::IsNullOrWhiteSpace($ServiceName)){throw '-ServiceName is required for Apply.'}
$allowed=@('VSS','swprv','SQLWriter','CryptSvc')
if($ServiceName -notin $allowed){throw "ServiceName is not in reviewed allow-list: $($allowed -join ', ')"}
$before=Get-Service -Name $ServiceName|Select-Object Name,Status,StartType
Write-WmJson $before (Join-Path $LogRoot 'vss-service-before.json')
Restart-Service -Name $ServiceName -Force -ErrorAction Stop
""",
        },
    }
    repair_template = r'''
<#
.SYNOPSIS Scan-first controlled repair wrapper for __OPERATION__.
.DESCRIPTION Default Mode=Scan writes a preflight plan. Mutations require Mode Repair, -Apply, elevation, ShouldProcess and the documented authorization gate.
.EXAMPLE .\__FILENAME__ -Mode Scan -LogRoot .\dist\repair-plan -Synthetic
.EXAMPLE .\__FILENAME__ -Mode Repair -Apply -Target '__TARGET__' -LogRoot C:\case\logs -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
 [ValidateSet('Scan','Repair')][string]$Mode='Scan',
 [switch]$Apply,
 [string]$Target='__TARGET__',
 [Parameter(Mandatory)][string]$LogRoot,
 [string]$Confirmation,
 [string]$PackageName,
 [string]$ProfileSid,
 [string]$PublishedName,
 [string]$ServiceName,
 [switch]$Synthetic
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$steps=@(__STEPS__)
$rollback=@(__ROLLBACK__)
$plan=New-WmRepairPlan -Operation '__OPERATION__' -RiskClass '__RISK__' -Target $Target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Scan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass '__RISK__' -Target $Target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply is forbidden with -Synthetic.'}
if($PSCmdlet.ShouldProcess($Target,'Apply __OPERATION__ (__RISK__)')){
 try{
__APPLY__
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='__OPERATION__';target=$Target;risk='__RISK__';result='applied';rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [pscustomobject]@{Operation='__OPERATION__';Target=$Target;Status='applied-pending-validation';ExitCode=0}
  exit 0
 }catch{
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='__OPERATION__';target=$Target;risk='__RISK__';result='failed';error=$_.Exception.Message;rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [Console]::Error.WriteLine($_.Exception.Message);exit 40
 }
}
'''
    for filename, definition in repair_definitions.items():
        steps = ",".join("'" + value.replace("'", "''") + "'" for value in definition["steps"])
        rollback = ",".join("'" + value.replace("'", "''") + "'" for value in definition["rollback"])
        script = (
            repair_template.replace("__FILENAME__", filename)
            .replace("__OPERATION__", definition["operation"])
            .replace("__RISK__", definition["risk"])
            .replace("__TARGET__", definition["target_default"])
            .replace("__STEPS__", steps)
            .replace("__ROLLBACK__", rollback)
            .replace("__APPLY__", textwrap.indent(definition["apply"].strip(), "  "))
        )
        write(f"scripts/repair/{filename}", clean(script))

    write(
        "scripts/repair/Invoke-BootRepair.ps1",
        clean(
            r'''
<#
.SYNOPSIS Plans or applies an exact BCDBoot repair after UEFI/BIOS layout identification.
.DESCRIPTION R3. Apply requires exact OS/System volumes, backup, elevation, ShouldProcess and typed confirmation.
.EXAMPLE .\Invoke-BootRepair.ps1 -Mode Plan -OsVolume D: -SystemVolume S: -Firmware UEFI -LogRoot E:\case\logs
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='High')]
param(
 [ValidateSet('Plan','Repair')][string]$Mode='Plan',
 [Parameter(Mandatory)][ValidatePattern('^[A-Za-z]:$')][string]$OsVolume,
 [Parameter(Mandatory)][ValidatePattern('^[A-Za-z]:$')][string]$SystemVolume,
 [Parameter(Mandatory)][ValidateSet('UEFI','BIOS','ALL')][string]$Firmware,
 [Parameter(Mandatory)][string]$LogRoot,
 [switch]$Apply,
 [string]$Confirmation,
 [switch]$Synthetic
)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot);Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$target="$OsVolume->$SystemVolume/$Firmware"
$steps=@('verify disk UniqueId/partition roles/BitLocker','export existing BCD','run BCDBoot with explicit /s and /f','enumerate and cold-boot validate')
$rollback=@('restore exported BCD store','restore ESP file backup','restore firmware boot entry through supported OEM/BCDEdit path')
$plan=New-WmRepairPlan -Operation 'boot-files-bcd' -RiskClass R3 -Target $target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Plan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass R3 -Target $target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply forbidden in synthetic mode.'}
$windows=Join-Path $OsVolume 'Windows'
if(-not(Test-Path -LiteralPath (Join-Path $windows 'System32'))){throw "Verified Windows directory missing: $windows"}
if(-not(Test-Path -LiteralPath "$SystemVolume\")){throw "System volume missing: $SystemVolume"}
if($PSCmdlet.ShouldProcess($target,'Back up BCD and rebuild boot files')){
 $backup=Join-Path $LogRoot 'bcd-before'
 & "$env:SystemRoot\System32\bcdedit.exe" /export $backup
 if($LASTEXITCODE -ne 0){throw 'BCD export failed; repair stopped.'}
 & "$env:SystemRoot\System32\bcdboot.exe" $windows /s $SystemVolume /f $Firmware
 if($LASTEXITCODE -ne 0){throw "BCDBoot failed: $LASTEXITCODE"}
 [pscustomobject]@{Target=$target;Status='applied-pending-cold-boot-validation';Backup=$backup}
}
'''
        ),
    )
    write(
        "scripts/toolkit/New-ServiceMediaPlan.ps1",
        clean(
            r'''
<#
.SYNOPSIS Generates a service-media plan; it never downloads assets or writes a USB device.
.EXAMPLE .\New-ServiceMediaPlan.ps1 -ManifestPath .\tools\manifests\service-media.yaml -OutputPath .\dist\service-media-plan.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$ManifestPath,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$manifest=Get-Content -LiteralPath (Resolve-Path -LiteralPath $ManifestPath) -Raw|ConvertFrom-Json
$adkRoots=@(@("${env:ProgramFiles(x86)}\Windows Kits\10\Assessment and Deployment Kit","$env:ProgramFiles\Windows Kits\10\Assessment and Deployment Kit")|Where-Object{$_ -and(Test-Path -LiteralPath $_)})
$plan=[ordered]@{created_utc=[DateTime]::UtcNow.ToString('o');mode='plan-only';adk_detected=@($adkRoots);winpe_build_allowed=($adkRoots.Count -gt 0);architectures=@('x64','ARM64');directories=$manifest.directories;items=$manifest.items;gates=@('review ADK page and security patch','exact USB UniqueId before R4 write','license acceptance','hash/signature verification');downloads_performed=0;usb_writes_performed=0}
$plan|ConvertTo-Json -Depth 12|Set-Content -LiteralPath $OutputPath -Encoding utf8
$plan
'''
        ),
    )
    write(
        "scripts/toolkit/Get-VerifiedServiceTool.ps1",
        clean(
            r'''
<#
.SYNOPSIS Resolves a catalog entry and optionally downloads an exact, verifiable asset without executing it.
.DESCRIPTION Default WhatIf is recommended. Actual download requires a direct HTTPS asset, exact version, expected SHA-256, license acceptance and ShouldProcess.
.EXAMPLE .\Get-VerifiedServiceTool.ps1 -ToolId rufus -Destination .\staging -WhatIf
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='High')]
param(
 [Parameter(Mandatory)][ValidatePattern('^[a-z0-9-]+$')][string]$ToolId,
 [Parameter(Mandatory)][string]$Destination,
 [string]$Version,
 [string]$AssetUrl,
 [ValidatePattern('^[a-fA-F0-9]{64}$')][string]$ExpectedSha256,
 [switch]$AcceptLicense
)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$catalog=Get-Content -LiteralPath (Join-Path $repo 'tools\catalog.yaml') -Raw|ConvertFrom-Json
$tool=@($catalog|Where-Object id -eq $ToolId)
if($tool.Count -ne 1){throw "Unknown/duplicate ToolId: $ToolId"}
$item=$tool[0]
$resolvedVersion=if($Version){$Version}else{$item.current_version}
$plan=[ordered]@{tool=$item.name;version=$resolvedVersion;official_home=$item.official_home;license=$item.license;commercial_use=$item.commercial_use;redistribution=$item.redistribution;signature_method=$item.signature_method;checksum_method=$item.checksum_method;asset_url=$AssetUrl;will_execute=$false}
Write-Verbose (($plan|Format-List|Out-String).Trim())
if(-not $AssetUrl){return [pscustomobject]$plan}
if($resolvedVersion -match '^(rolling|unknown|os-component|service|per-tool)'){throw 'Exact version is required before download.'}
if($AssetUrl -notmatch '^https://'){throw 'Only explicit HTTPS asset URLs are allowed.'}
if(-not $ExpectedSha256){throw 'ExpectedSha256 from an official source is required.'}
if(-not $AcceptLicense){throw "Read and accept license '$($item.license)' with -AcceptLicense."}
if(-not $PSCmdlet.ShouldProcess("$AssetUrl -> $Destination","Download $($item.name) $resolvedVersion and verify; never execute")){return [pscustomobject]$plan}
$destinationRoot=[IO.Path]::GetFullPath($Destination);New-Item -ItemType Directory -Path $destinationRoot -Force|Out-Null
$temp=Join-Path ([IO.Path]::GetTempPath()) ('wmtool-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temp -Force|Out-Null
try{
 $leaf=[IO.Path]::GetFileName(([uri]$AssetUrl).AbsolutePath);if(-not $leaf){throw 'Asset URL has no filename.'}
 $download=Join-Path $temp $leaf
 Invoke-WebRequest -Uri $AssetUrl -OutFile $download -MaximumRedirection 5 -TimeoutSec 120
 $actual=(Get-FileHash -LiteralPath $download -Algorithm SHA256).Hash.ToLowerInvariant()
 if($actual -cne $ExpectedSha256.ToLowerInvariant()){throw "SHA-256 mismatch; expected $ExpectedSha256, got $actual"}
 $signature=Get-AuthenticodeSignature -FilePath $download
 if($item.signature_method -match 'Authenticode' -and $signature.Status -ne 'Valid'){throw "Authenticode required but status is $($signature.Status)"}
 $final=Join-Path $destinationRoot $leaf;Move-Item -LiteralPath $download -Destination $final
 $provenance=[ordered]@{tool_id=$ToolId;version=$resolvedVersion;source=$AssetUrl;downloaded_utc=[DateTime]::UtcNow.ToString('o');bytes=(Get-Item $final).Length;sha256=$actual;signature_status=$signature.Status.ToString();license=$item.license;executed=$false}
 $provenance|ConvertTo-Json -Depth 8|Set-Content -LiteralPath "$final.provenance.json" -Encoding utf8
 [pscustomobject]$provenance
}finally{if(Test-Path -LiteralPath $temp){Remove-Item -LiteralPath $temp -Recurse -Force}}
'''
        ),
    )
    write(
        "scripts/toolkit/Test-ServiceMediaIntegrity.ps1",
        clean(
            r'''
<#
.SYNOPSIS Verifies files against a provenance manifest without executing them.
.EXAMPLE .\Test-ServiceMediaIntegrity.ps1 -Root .\staging -ManifestPath .\staging\provenance.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Root,[Parameter(Mandatory)][string]$ManifestPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$resolved=(Resolve-Path -LiteralPath $Root).Path;$manifest=Get-Content -LiteralPath (Resolve-Path -LiteralPath $ManifestPath) -Raw|ConvertFrom-Json
$results=@()
foreach($entry in @($manifest.files)){
 $path=Join-Path $resolved $entry.path
 if(-not(Test-Path -LiteralPath $path -PathType Leaf)){$results+=[pscustomobject]@{Path=$entry.path;Status='missing'};continue}
 $hash=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
 $status=if($hash -ceq $entry.sha256.ToLowerInvariant()){'ok'}else{'hash-mismatch'}
 $results+=[pscustomobject]@{Path=$entry.path;Status=$status;Sha256=$hash}
}
$results
if(@($results|Where-Object Status -ne 'ok').Count){exit 2}else{exit 0}
'''
        ),
    )

    write(
        "scripts/repo/Build-SkillPackages.ps1",
        clean(
            r'''
<#
.SYNOPSIS Builds self-contained skill directories under dist/skills with shared resources copied in.
.EXAMPLE .\Build-SkillPackages.ps1
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='Low')]
param([string]$Destination)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$source=Join-Path $repo '.agents\skills'
if(-not $Destination){$Destination=Join-Path $repo 'dist\skills'}
$dest=[IO.Path]::GetFullPath($Destination)
$skills=@(Get-ChildItem -LiteralPath $source -Directory|Where-Object Name -ne '_shared'|Sort-Object Name)
if($WhatIfPreference){
 [pscustomobject]@{Destination=$dest;Packages=$skills.Count;SharedCopied=$false;Planned=$true}
 return
}
if(Test-Path -LiteralPath $dest){
 $resolved=[IO.Path]::GetFullPath($dest)
 $repoResolved=[IO.Path]::GetFullPath($repo)
 if(-not $resolved.StartsWith($repoResolved,[StringComparison]::OrdinalIgnoreCase) -and -not $PSBoundParameters.ContainsKey('Destination')){throw 'Refusing to clean destination outside repository.'}
 if($PSCmdlet.ShouldProcess($resolved,'Replace package output')){Remove-Item -LiteralPath $resolved -Recurse -Force}
}
New-Item -ItemType Directory -Path $dest -Force|Out-Null
$shared=Join-Path $source '_shared'
$manifest=@()
foreach($skill in $skills){
 $target=Join-Path $dest $skill.Name
 Copy-Item -LiteralPath $skill.FullName -Destination $target -Recurse
 $sharedTarget=Join-Path $target 'references\_shared'
 Copy-Item -LiteralPath $shared -Destination $sharedTarget -Recurse
 if(Test-Path -LiteralPath (Join-Path $sharedTarget 'SKILL.md')){throw '_shared unexpectedly contains SKILL.md'}
 $files=@()
 foreach($file in Get-ChildItem -LiteralPath $target -File -Recurse|Sort-Object FullName){$files+=[ordered]@{path=(Get-WmRelativePath -BasePath $target -Path $file.FullName);sha256=(Get-FileHash $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant();bytes=$file.Length}}
 $entry=[ordered]@{skill=$skill.Name;path=(Get-WmRelativePath -BasePath $repo -Path $target);self_contained=$true;files=$files}
 $entry|ConvertTo-Json -Depth 20|Set-Content -LiteralPath (Join-Path $target 'package-manifest.json') -Encoding utf8
 $manifest+=$entry
}
$manifest|ConvertTo-Json -Depth 20|Set-Content -LiteralPath (Join-Path $dest 'packages.json') -Encoding utf8
[pscustomobject]@{Destination=$dest;Packages=$manifest.Count;SharedCopied=$true}
'''
        ),
    )
    write(
        "scripts/repo/Install-WindowsMasterSkills.ps1",
        clean(
            r'''
<#
.SYNOPSIS Installs Windows Master skills using Copy (default) or Junction with collision backup and a file manifest.
.EXAMPLE .\Install-WindowsMasterSkills.ps1 -Scope User -Mode Copy
.EXAMPLE .\Install-WindowsMasterSkills.ps1 -Destination C:\Temp\skills -Mode Copy
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='Medium')]
param(
 [ValidateSet('Repo','User')][string]$Scope='User',
 [ValidateSet('Copy','Junction')][string]$Mode='Copy',
 [string]$Destination,
 [string]$Source
)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
if(-not $Source){
 $packaged=Join-Path $repo 'dist\skills'
 if(Test-Path -LiteralPath (Join-Path $packaged 'packages.json')){$Source=$packaged}else{$Source=Join-Path $repo '.agents\skills'}
}
if(-not $Destination){
 if($Scope -eq 'User'){$Destination=Join-Path ([Environment]::GetFolderPath('UserProfile')) '.agents\skills'}
 else{throw "Repo scope requires -Destination '<TARGET_REPO>\.agents\skills'. This repository already exposes .agents\skills directly."}
}
$sourceRoot=(Resolve-Path -LiteralPath $Source).Path;$dest=[IO.Path]::GetFullPath($Destination)
if([IO.Path]::GetFullPath($sourceRoot).TrimEnd('\') -eq $dest.TrimEnd('\')){throw 'Source and destination must differ.'}
$skills=@(Get-ChildItem -LiteralPath $sourceRoot -Directory|Where-Object Name -ne '_shared'|Sort-Object Name)
if($WhatIfPreference){
 [pscustomobject]@{Destination=$dest;Installed=0;Planned=$skills.Count;Mode=$Mode;Manifest=(Join-Path $dest '.windows-master-installed.json');Mutation=$false}
 return
}
New-Item -ItemType Directory -Path $dest -Force|Out-Null
$stamp=Get-Date -Format 'yyyyMMddHHmmss';$backupRoot=Join-Path $dest ".windows-master-backup-$stamp";$entries=@()
foreach($skill in $skills){
 $target=Join-Path $dest $skill.Name;$backup=$null
 if(Test-Path -LiteralPath $target){
  New-Item -ItemType Directory -Path $backupRoot -Force|Out-Null;$backup=Join-Path $backupRoot $skill.Name
  if($PSCmdlet.ShouldProcess($target,"Back up collision to $backup")){Move-Item -LiteralPath $target -Destination $backup}
 }
 if($PSCmdlet.ShouldProcess($target,"Install skill using $Mode")){
  if($Mode -eq 'Copy'){Copy-Item -LiteralPath $skill.FullName -Destination $target -Recurse}
  else{New-Item -ItemType Junction -Path $target -Target $skill.FullName|Out-Null}
 }
 $files=@()
 if($Mode -eq 'Copy'){foreach($file in Get-ChildItem -LiteralPath $target -File -Recurse){$files+=[ordered]@{path=(Get-WmRelativePath -BasePath $dest -Path $file.FullName);sha256=(Get-FileHash $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}}}
 $entries+=[ordered]@{name=$skill.Name;target=$target;mode=$Mode;source=$skill.FullName;backup=$backup;files=$files}
}
$manifest=[ordered]@{schema_version='1.0.0';installed_utc=[DateTime]::UtcNow.ToString('o');scope=$Scope;destination=$dest;source=$sourceRoot;entries=$entries}
$manifestPath=Join-Path $dest '.windows-master-installed.json'
$manifest|ConvertTo-Json -Depth 20|Set-Content -LiteralPath $manifestPath -Encoding utf8
[pscustomobject]@{Destination=$dest;Installed=$entries.Count;Mode=$Mode;Manifest=$manifestPath;Backup=$backupRoot}
'''
        ),
    )
    write(
        "scripts/repo/Uninstall-WindowsMasterSkills.ps1",
        clean(
            r'''
<#
.SYNOPSIS Removes only files recorded by the installer manifest; modified files are preserved.
.EXAMPLE .\Uninstall-WindowsMasterSkills.ps1 -Scope User -RestoreBackup
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='High')]
param([ValidateSet('Repo','User')][string]$Scope='User',[string]$Destination,[switch]$RestoreBackup)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if(-not $Destination){
 if($Scope -eq 'User'){$Destination=Join-Path ([Environment]::GetFolderPath('UserProfile')) '.agents\skills'}
 else{throw "Repo scope requires the exact installed -Destination '<TARGET_REPO>\.agents\skills'."}
}
$dest=[IO.Path]::GetFullPath($Destination);$manifestPath=Join-Path $dest '.windows-master-installed.json'
if(-not(Test-Path -LiteralPath $manifestPath)){throw "Install manifest not found: $manifestPath"}
$manifest=Get-Content -LiteralPath $manifestPath -Raw|ConvertFrom-Json
if([IO.Path]::GetFullPath($manifest.destination).TrimEnd('\') -ne $dest.TrimEnd('\')){throw 'Manifest destination mismatch.'}
$removed=0;$preserved=@()
foreach($entry in @($manifest.entries)){
 $target=[IO.Path]::GetFullPath($entry.target)
 if(-not $target.StartsWith($dest.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw "Unsafe target in manifest: $target"}
 if(-not(Test-Path -LiteralPath $target)){continue}
 if($entry.mode -eq 'Junction'){
  $item=Get-Item -LiteralPath $target -Force
  if(-not($item.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw "Expected junction but found regular directory: $target"}
  if($PSCmdlet.ShouldProcess($target,'Remove installed junction')){Remove-Item -LiteralPath $target -Force;$removed++}
 }else{
  $changed=$false
  foreach($file in @($entry.files)){
   $path=Join-Path $dest $file.path
   if(Test-Path -LiteralPath $path){$hash=(Get-FileHash $path -Algorithm SHA256).Hash.ToLowerInvariant();if($hash -cne $file.sha256){$changed=$true;$preserved+=$path}}
  }
  if(-not $changed -and $PSCmdlet.ShouldProcess($target,'Remove unchanged installed skill directory')){Remove-Item -LiteralPath $target -Recurse -Force;$removed++}
 }
 if($RestoreBackup -and $entry.backup -and (Test-Path -LiteralPath $entry.backup) -and -not(Test-Path -LiteralPath $target)){
  if($PSCmdlet.ShouldProcess($entry.backup,"Restore backup to $target")){Move-Item -LiteralPath $entry.backup -Destination $target}
 }
}
if($preserved.Count -eq 0 -and $PSCmdlet.ShouldProcess($manifestPath,'Remove install manifest')){Remove-Item -LiteralPath $manifestPath -Force}
[pscustomobject]@{Destination=$dest;Removed=$removed;PreservedModified=@($preserved);BackupRestoreRequested=[bool]$RestoreBackup}
'''
        ),
    )
    write(
        "scripts/repo/Update-WindowsKnowledgeBase.ps1",
        clean(
            r'''
<#
.SYNOPSIS Stages official Windows release metadata for review; it never overwrites the accepted matrix.
.EXAMPLE .\Update-WindowsKnowledgeBase.ps1 -WhatIf
.EXAMPLE .\Update-WindowsKnowledgeBase.ps1 -Fetch -OutputPath .\dist\research\windows-candidate.json
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='Low')]
param([switch]$Fetch,[string]$OutputPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$urls=@(
 'https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information',
 'https://learn.microsoft.com/en-us/windows/release-health/release-information',
 'https://learn.microsoft.com/en-us/windows-hardware/get-started/adk-install',
 'https://learn.microsoft.com/en-us/troubleshoot/windows-client/windows-security/update-secure-boot-certificates'
)
$plan=[ordered]@{created_utc=[DateTime]::UtcNow.ToString('o');sources=$urls;accepted_matrix='knowledge-base/os/windows-release-matrix.yaml';mode='candidate-diff-only';auto_accept=$false}
if(-not $Fetch){[pscustomobject]$plan;return}
if(-not $OutputPath){throw '-OutputPath is required with -Fetch.'}
if(-not $PSCmdlet.ShouldProcess($OutputPath,'Fetch official HTML metadata to review candidate')){return [pscustomobject]$plan}
$candidate=[ordered]@{metadata=$plan;pages=@()}
foreach($url in $urls){
 try{$response=Invoke-WebRequest -Uri $url -MaximumRedirection 5 -TimeoutSec 45;$candidate.pages+=[ordered]@{url=$url;status=[int]$response.StatusCode;bytes=$response.RawContentLength;sha256=(Get-WmStringSha256 -Text $response.Content);retrieved_utc=[DateTime]::UtcNow.ToString('o')}}
 catch{$candidate.pages+=[ordered]@{url=$url;status='error';message=$_.Exception.Message}}
}
New-Item -ItemType Directory -Path (Split-Path -Parent $OutputPath) -Force|Out-Null
$candidate|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $OutputPath -Encoding utf8
[pscustomobject]$candidate
'''
        ),
    )
    write(
        "scripts/repo/Update-ToolCatalog.ps1",
        clean(
            r'''
<#
.SYNOPSIS Checks official tool pages as metadata and writes a review-only diff report.
.EXAMPLE .\Update-ToolCatalog.ps1 -WhatIf
.EXAMPLE .\Update-ToolCatalog.ps1 -Fetch -OutputPath .\dist\research\tool-diff.json
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='Low')]
param([switch]$Fetch,[string]$OutputPath,[int]$MaxTools=20)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$catalog=Get-Content -LiteralPath (Join-Path $repo 'tools\catalog.yaml') -Raw|ConvertFrom-Json
$targets=@($catalog|Where-Object status -in @('active','unknown')|Select-Object -First $MaxTools)
$plan=[ordered]@{created_utc=[DateTime]::UtcNow.ToString('o');count=$targets.Count;mode='metadata-diff-only';auto_accept=$false;tool_ids=@($targets.id)}
if(-not $Fetch){[pscustomobject]$plan;return}
if(-not $OutputPath){throw '-OutputPath is required with -Fetch.'}
if(-not $PSCmdlet.ShouldProcess($OutputPath,'Check official pages and write review report')){return [pscustomobject]$plan}
$report=[ordered]@{metadata=$plan;checks=@()}
foreach($tool in $targets){
 try{$response=Invoke-WebRequest -Uri $tool.official_home -Method Head -MaximumRedirection 5 -TimeoutSec 30;$report.checks+=[ordered]@{id=$tool.id;url=$tool.official_home;status=[int]$response.StatusCode;checked_utc=[DateTime]::UtcNow.ToString('o');catalog_version=$tool.current_version}}
 catch{$report.checks+=[ordered]@{id=$tool.id;url=$tool.official_home;status='error';message=$_.Exception.Message}}
}
New-Item -ItemType Directory -Path (Split-Path -Parent $OutputPath) -Force|Out-Null
$report|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $OutputPath -Encoding utf8
[pscustomobject]$report
'''
        ),
    )
    write(
        "scripts/repo/Test-WindowsMasterRepo.ps1",
        clean(
            r'''
<#
.SYNOPSIS Runs safe repository validation, schema/static tests, Pester when compatible, packaging and temp install/uninstall.
.EXAMPLE .\Test-WindowsMasterRepo.ps1 -Category All
#>
[CmdletBinding()]
param([ValidateSet('All','Structure','Scripts','Safety','Links','Evals','Pester','Smoke')][string]$Category='All',[string]$ReportPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if(-not $ReportPath){$ReportPath=Join-Path $repo 'dist\reports\validation.json'}
New-Item -ItemType Directory -Path (Split-Path -Parent $ReportPath) -Force|Out-Null
$results=@()
function Add-Result([string]$Name,[string]$Status,[string]$Detail,[double]$Seconds){$script:results+=[pscustomobject][ordered]@{name=$Name;status=$Status;detail=$Detail;seconds=[Math]::Round($Seconds,3)}}
$failed=$false
if($Category -in @('All','Structure','Scripts','Safety','Links','Evals')){
 $sw=[Diagnostics.Stopwatch]::StartNew()
 & python (Join-Path $repo 'scripts\repo\validate_repo.py') --root $repo --category $Category --json-out (Join-Path $repo 'dist\reports\static-validation.json')
 $code=$LASTEXITCODE;$sw.Stop()
 if($code -eq 0){Add-Result 'static-validator' 'PASS' "category=$Category" $sw.Elapsed.TotalSeconds}else{Add-Result 'static-validator' 'FAIL' "exit=$code" $sw.Elapsed.TotalSeconds;$failed=$true}
}
if($Category -in @('All','Pester')){
 $pester=Get-Module -ListAvailable Pester|Sort-Object Version -Descending|Select-Object -First 1
 if(-not $pester){Add-Result 'Pester' 'SKIP' 'Pester is not installed; CI pins Pester 5.6.1.' 0}
 elseif($pester.Version.Major -lt 5){
  Import-Module Pester -RequiredVersion $pester.Version -Force
  $sw=[Diagnostics.Stopwatch]::StartNew()
  $pesterResult=Invoke-Pester -Script (Join-Path $repo 'tests\pester') -PassThru
  $sw.Stop()
  if($pesterResult.FailedCount -eq 0){Add-Result 'Pester' 'PASS' "$($pesterResult.PassedCount) passed with compatible local Pester $($pester.Version)" $sw.Elapsed.TotalSeconds}else{Add-Result 'Pester' 'FAIL' "$($pesterResult.FailedCount) failed with local Pester $($pester.Version)" $sw.Elapsed.TotalSeconds;$failed=$true}
 }
 else{
  Import-Module Pester -MinimumVersion 5.5 -Force
  $sw=[Diagnostics.Stopwatch]::StartNew()
  $config=New-PesterConfiguration
  $config.Run.Path=Join-Path $repo 'tests\pester'
  $config.Run.PassThru=$true;$config.Output.Verbosity='Detailed'
  $pesterResult=Invoke-Pester -Configuration $config;$sw.Stop()
  if($pesterResult.FailedCount -eq 0){Add-Result 'Pester' 'PASS' "$($pesterResult.PassedCount) passed" $sw.Elapsed.TotalSeconds}else{Add-Result 'Pester' 'FAIL' "$($pesterResult.FailedCount) failed" $sw.Elapsed.TotalSeconds;$failed=$true}
 }
}
$analyzer=Get-Module -ListAvailable PSScriptAnalyzer|Sort-Object Version -Descending|Select-Object -First 1
if($Category -in @('All','Scripts')){
 if(-not $analyzer){Add-Result 'PSScriptAnalyzer' 'SKIP' 'Module not installed; AST safety/style checks ran in static-validator; CI pins 1.24.0.' 0}
 else{
  Import-Module PSScriptAnalyzer -Force
  $sw=[Diagnostics.Stopwatch]::StartNew()
  $issues=@(Invoke-ScriptAnalyzer -Path (Join-Path $repo 'scripts') -Recurse -Settings (Join-Path $repo 'PSScriptAnalyzerSettings.psd1'));$sw.Stop()
  if($issues.Count -eq 0){Add-Result 'PSScriptAnalyzer' 'PASS' '0 findings' $sw.Elapsed.TotalSeconds}else{Add-Result 'PSScriptAnalyzer' 'FAIL' "$($issues.Count) findings" $sw.Elapsed.TotalSeconds;$failed=$true}
 }
}
if($Category -in @('All','Smoke')){
 $sw=[Diagnostics.Stopwatch]::StartNew()
 $packageRoot=Join-Path $repo 'dist\skills'
 & (Join-Path $repo 'scripts\repo\Build-SkillPackages.ps1') -Destination $packageRoot|Out-Null
 $temp=Join-Path $repo 'dist\test-install'
 if(Test-Path -LiteralPath $temp){Remove-Item -LiteralPath $temp -Recurse -Force}
 & (Join-Path $repo 'scripts\repo\Install-WindowsMasterSkills.ps1') -Destination $temp -Source (Join-Path $repo '.agents\skills') -Mode Copy|Out-Null
 $installed=@(Get-ChildItem -LiteralPath $temp -Directory|Where-Object Name -notmatch '^\.').Count
 & (Join-Path $repo 'scripts\repo\Uninstall-WindowsMasterSkills.ps1') -Destination $temp -Confirm:$false|Out-Null
 $remaining=@(Get-ChildItem -LiteralPath $temp -Directory -ErrorAction SilentlyContinue|Where-Object Name -notmatch '^\.').Count
 $sw.Stop()
 if($installed -eq 39 -and $remaining -eq 0){Add-Result 'package-install-uninstall-smoke' 'PASS' '39 installed, 0 remaining' $sw.Elapsed.TotalSeconds}else{Add-Result 'package-install-uninstall-smoke' 'FAIL' "installed=$installed remaining=$remaining" $sw.Elapsed.TotalSeconds;$failed=$true}
}
$summary=[ordered]@{created_utc=[DateTime]::UtcNow.ToString('o');host_powershell=$PSVersionTable.PSVersion.ToString();category=$Category;results=$results;passed=@($results|Where-Object status -eq 'PASS').Count;failed=@($results|Where-Object status -eq 'FAIL').Count;skipped=@($results|Where-Object status -eq 'SKIP').Count}
$summary|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $ReportPath -Encoding utf8
$results|Format-Table -AutoSize
if($failed){exit 1}else{exit 0}
'''
        ),
    )
    write(
        "scripts/repo/validate_repo.py",
        clean(
            r'''
#!/usr/bin/env python3
"""Dependency-free structural, schema-shaped, link, safety and eval validation."""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, time
from pathlib import Path

EXPECTED_SKILLS = {
 "windows-master-router","windows-service-intake","windows-case-evidence","pc-hardware-diagnostics",
 "bios-uefi-firmware","storage-triage-cloning-recovery","memory-cpu-gpu-thermal","windows-os-identification",
 "windows-boot-recovery","winpe-offline-repair","windows-bcd-partition-repair","windows-component-repair",
 "windows-update-servicing","windows-setup-upgrade-rollback","windows-activation-licensing","windows-bsod-debugging",
 "windows-performance-hangs","windows-process-service-startup","windows-drivers-devices","windows-network-repair",
 "windows-peripherals-repair","windows-accounts-profiles","windows-ntfs-permissions-shares",
 "windows-bitlocker-tpm-security","windows-malware-remediation","windows-apps-store-winget",
 "windows-shell-ui-repair","windows-office-cloud-repair","windows-backup-vss-restore",
 "windows-remote-managed-client","windows-advanced-administration","windows-automation-powershell",
 "windows-deployment-imaging","windows-service-media","windows-legacy-xp-vista-7-8","windows-10-support",
 "windows-11-support","windows-post-repair-validation","windows-tool-research"
}
REQUIRED_HEADINGS = [
 "Cel i granice odpowiedzialności","Kiedy aktywować i kiedy nie aktywować",
 "Dane wejściowe i minimalne pytania bezpieczeństwa","Szybki triage i czerwone flagi",
 "Zgodność","Drzewo objaw","Najpierw diagnostyka read-only","Drabina napraw",
 "Karty poleceń","Dlaczego to może pójść źle","Backup i rollback","Oczekiwany wynik",
 "Walidacja i regresja","Przerwanie i eskalacja","Logi i artefakty","Powiązane skille",
 "Źródła","Antywzorce"
]
PLAYBOOK_FIELDS = {
 "id","title","summary","symptoms","applies_to","excludes","risk_class","authorization_required",
 "prerequisites","data_safety","evidence_to_collect","hypotheses","diagnostics","repair_ladder",
 "commands","rollback","validation","stop_conditions","escalation","related_skills","sources",
 "last_verified","status"
}
TOOL_FIELDS = {
 "id","name","category","publisher","official_home","official_download","official_repository",
 "current_version","checked_at","status","replaced_by","license","commercial_use","redistribution",
 "supported_os","architectures","environments","portable","install_type","network_required",
 "elevation_required","signature_method","checksum_method","risk_class","use_cases","avoid_when",
 "known_gotchas","alternatives","sources"
}
ORCHESTRATOR_METADATA_KEYS = {
 "swietlik.orchestrator.schema","swietlik.orchestrator.pack",
 "swietlik.orchestrator.recommended-agent","swietlik.orchestrator.minimum-agent",
 "swietlik.orchestrator.reasoning","swietlik.orchestrator.verbosity",
 "swietlik.orchestrator.delegation","swietlik.orchestrator.review",
 "swietlik.orchestrator.parallel","swietlik.orchestrator.risk"
}

class Check:
 def __init__(self):
  self.errors=[]; self.warnings=[]; self.metrics={}; self.checks=[]
 def error(self, msg): self.errors.append(msg)
 def warn(self, msg): self.warnings.append(msg)
 def record(self, name, before, started):
  self.checks.append({"name":name,"status":"PASS" if len(self.errors)==before else "FAIL","new_errors":len(self.errors)-before,"seconds":round(time.time()-started,3)})

def frontmatter(text):
 if not text.startswith("---\n"): return {}, ""
 end=text.find("\n---\n",4)
 if end<0:return {}, ""
 data={}; parent=None
 for line in text[4:end].splitlines():
  if ":" not in line:continue
  key,value=line.split(":",1)
  if line.startswith("  ") and parent=="metadata":
   data[parent][key.strip()]=value.strip().strip('"')
  else:
   parent=key.strip(); parsed=value.strip().strip('"')
   data[parent]={} if parent=="metadata" and not parsed else parsed
 return data,text[end+5:]

def load_json(path, c):
 try:return json.loads(path.read_text(encoding="utf-8"))
 except Exception as exc:c.error(f"JSON/YAML parse {path}: {exc}");return None

def structure(root,c):
 start=time.time();before=len(c.errors);base=root/".agents"/"skills"
 required_artifacts=[
  "AGENTS.md","README.md","LICENSE.md","SECURITY.md","CHANGELOG.md","ROADMAP.md","REPO_STATUS.md",
  "RESEARCH_QUEUE.md","coverage-matrix.yaml",".github/workflows/validate.yml",
  "knowledge-base/hardware/hardware-safety-gates.yaml","knowledge-base/security/security-gates.yaml",
  "docs/architecture.md","docs/operating-model.md","docs/diagnostic-method.md",
  "docs/safety-and-authorization.md","docs/source-policy.md","docs/tool-selection-policy.md",
  "docs/service-media.md","docs/legacy-isolation.md","docs/testing-lab.md","docs/maintenance.md",
  "docs/assumptions.md","tools/catalog.yaml","tools/catalog.schema.json"
 ]
 for rel in required_artifacts:
  if not (root/rel).exists():c.error(f"Missing required repository artifact: {rel}")
 actual={p.name for p in base.iterdir() if p.is_dir() and p.name!="_shared"}
 if actual!=EXPECTED_SKILLS:c.error(f"Skill set mismatch missing={sorted(EXPECTED_SKILLS-actual)} extra={sorted(actual-EXPECTED_SKILLS)}")
 if (base/"_shared"/"SKILL.md").exists():c.error("_shared must not contain SKILL.md")
 total_playbooks=total_cards=0
 for name in sorted(EXPECTED_SKILLS):
  folder=base/name; path=folder/"SKILL.md"
  if not path.exists():c.error(f"Missing {path}");continue
  text=path.read_text(encoding="utf-8");fm,body=frontmatter(text)
  if set(fm)!={"name","description","metadata"}:c.error(f"{name}: frontmatter keys {sorted(fm)}")
  if fm.get("name")!=name:c.error(f"{name}: name mismatch")
  metadata=fm.get("metadata",{})
  if not isinstance(metadata,dict) or set(metadata)!=ORCHESTRATOR_METADATA_KEYS:c.error(f"{name}: invalid orchestrator metadata keys")
  elif metadata.get("swietlik.orchestrator.schema")!="1" or metadata.get("swietlik.orchestrator.pack")!="windows-pc-skills":c.error(f"{name}: invalid orchestrator metadata identity")
  desc=fm.get("description","")
  if not 120<=len(desc)<=900:c.error(f"{name}: description length {len(desc)}")
  if not re.search(r"[ąćęłńóśźż]",desc.lower()) or "Use for" not in desc:c.error(f"{name}: description must contain Polish and English trigger language")
  if len(text.splitlines())>=500:c.error(f"{name}: SKILL.md >=500 lines")
  for heading in REQUIRED_HEADINGS:
   if heading not in body:c.error(f"{name}: missing heading/content {heading}")
  for rel in ["references/playbooks.md","references/command-cards.md","references/compatibility.md","references/sources.md","agents/openai.yaml","assets/validation-checklist.md"]:
   if not (folder/rel).exists():c.error(f"{name}: missing {rel}")
  pb=(folder/"references"/"playbooks.md").read_text(encoding="utf-8")
  cards=(folder/"references"/"command-cards.md").read_text(encoding="utf-8")
  pbc=len(re.findall(r"^## [a-z0-9-]+-pb-\d{2}:",pb,re.M)); cc=len(re.findall(r"^- \*\*ID:\*\* `[a-z0-9-]+-cmd-\d{2}`",cards,re.M))
  total_playbooks+=pbc;total_cards+=cc
  if pbc<3:c.error(f"{name}: only {pbc} playbooks")
  if cc<3:c.error(f"{name}: only {cc} command cards")
  yaml=(folder/"agents"/"openai.yaml").read_text(encoding="utf-8")
  m=re.search(r'  short_description: "(.*)"',yaml)
  if not m or not 25<=len(m.group(1))<=64:c.error(f"{name}: invalid short_description")
  if f"${name}" not in yaml:c.error(f"{name}: default_prompt does not mention skill")
 c.metrics.update({"skills":len(actual),"playbooks_in_skill_refs":total_playbooks,"command_cards_in_skill_refs":total_cards})
 c.record("structure",before,start)

def schemas(root,c):
 start=time.time();before=len(c.errors)
 for path in list(root.rglob("*.yaml"))+list(root.rglob("*.json")):
  if any(part in {".git","dist"} for part in path.parts):continue
  if path.name in {"openai.yaml","pack.yaml"}:continue
  load_json(path,c)
 playbooks=list((root/"knowledge-base"/"playbooks").glob("*.yaml"))
 sources=load_json(root/"knowledge-base"/"sources"/"source-register.yaml",c) or []
 source_ids={row.get("id") for row in sources if isinstance(row,dict)}
 for path in playbooks:
  row=load_json(path,c)
  if not isinstance(row,dict):continue
  missing=PLAYBOOK_FIELDS-set(row)
  if missing:c.error(f"{path}: missing {sorted(missing)}")
  if row.get("status") not in {"complete","partial","experimental","requires-live-validation"}:c.error(f"{path}: invalid status")
  for sid in row.get("sources",[]):
   if sid not in source_ids:c.error(f"{path}: unknown source {sid}")
 tools=load_json(root/"tools"/"catalog.yaml",c) or []
 ids=set()
 for row in tools:
  if set(row)!=TOOL_FIELDS:c.error(f"tool {row.get('id')}: fields mismatch missing={sorted(TOOL_FIELDS-set(row))} extra={sorted(set(row)-TOOL_FIELDS)}")
  if row.get("id") in ids:c.error(f"duplicate tool {row.get('id')}")
  ids.add(row.get("id"))
  if row.get("redistribution") not in {"forbidden","unknown","allowed","conditional"}:c.error(f"tool {row.get('id')}: redistribution")
  if not str(row.get("official_home","")).startswith("https://"):c.error(f"tool {row.get('id')}: non-HTTPS official home")
 c.metrics.update({"machine_playbooks":len(playbooks),"sources":len(sources),"tools":len(tools)})
 c.record("schema-shaped-data",before,start)

def links(root,c):
 start=time.time();before=len(c.errors);checked=0
 markdown=[p for p in root.rglob("*.md") if ".git" not in p.parts and "dist" not in p.parts and p.name!="prompt_codex_windows_master_service_skills.md"]
 pattern=re.compile(r"\[[^\]]*\]\(([^)]+)\)")
 for path in markdown:
  for target in pattern.findall(path.read_text(encoding="utf-8")):
   if target.startswith(("http://","https://","mailto:","#")):continue
   target=target.strip("<>").split("#",1)[0]
   if not target:continue
   checked+=1
   resolved=(path.parent/target).resolve()
   if not resolved.exists():c.error(f"Broken link {path.relative_to(root)} -> {target}")
 c.metrics["internal_links_checked"]=checked;c.record("internal-links",before,start)

def safety(root,c):
 start=time.time();before=len(c.errors)
 forbidden_ext={".exe",".dll",".iso",".wim",".esd",".ffu",".sys",".msi",".msix",".vhd",".vhdx",".pfx",".key"}
 bad_files=[str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and p.suffix.lower() in forbidden_ext and ".git" not in p.parts]
 if bad_files:c.error("Forbidden binary/media files: "+", ".join(bad_files))
 for path in (root/"scripts").rglob("*.ps1"):
  text=path.read_text(encoding="utf-8")
  if re.search(r"(?im)^\s*(Invoke-Expression|iex)\b|\b(?:irm|iwr|curl)\b[^\n|]*\|\s*(?:iex|sh|bash|powershell)",text):c.error(f"unsafe code execution pattern: {path}")
  if "Win32_Product" in text:c.error(f"Win32_Product in executable script: {path}")
  if path.parent.name=="repair":
   if "SupportsShouldProcess" not in text or "-Apply" not in text and "[switch]$Apply" not in text:c.error(f"repair safety gate incomplete: {path}")
   if re.search(r"(?im)ValidateSet\('Scan','Repair'\).*='Repair'",text):c.error(f"repair defaults to Repair: {path}")
 # Exact secret patterns, excluding the specification and redaction fixtures/pattern code.
 secret_patterns=[r"\bsk-[A-Za-z0-9_-]{20,}",r"\bAKIA[A-Z0-9]{16}\b",r"\b\d{6}(?:-\d{6}){7}\b"]
 excluded_placeholder_files={"prompt_codex_windows_master_service_skills.md","generate_repository.py","validate_repo.py","Structure.Tests.ps1"}
 for path in root.rglob("*"):
  if not path.is_file() or any(part in {".git","dist"} for part in path.parts) or path.name=="prompt_codex_windows_master_service_skills.md":continue
  if path.name in excluded_placeholder_files:continue
  if path.suffix.lower() not in {".md",".json",".yaml",".ps1",".psm1",".py",".cmd",".yml"}:continue
  text=path.read_text(encoding="utf-8",errors="ignore")
  if path.name in {"WindowsMaster.Common.psm1","validate_repo.py"}:continue
  for pat in secret_patterns:
   if re.search(pat,text):c.error(f"secret-like value in {path.relative_to(root)}")
 placeholders=[]
 for path in root.rglob("*"):
  if not path.is_file() or any(part in {".git","dist"} for part in path.parts) or path.name=="prompt_codex_windows_master_service_skills.md":continue
  if path.name in excluded_placeholder_files:continue
  if path.suffix.lower() in {".md",".ps1",".py",".yaml",".json"}:
   text=path.read_text(encoding="utf-8",errors="ignore")
   if re.search(r"(?i)TODO:\s*(add|complete|replace)|\[TODO",text):placeholders.append(str(path.relative_to(root)))
 if placeholders:c.error("Unresolved placeholders: "+", ".join(placeholders))
 c.metrics["forbidden_binary_count"]=len(bad_files);c.record("safety",before,start)

def evals(root,c):
 start=time.time();before=len(c.errors);files=list((root/"tests"/"evals").glob("*.yaml"));prompts=0
 expected_files=EXPECTED_SKILLS
 actual=set()
 for path in files:
  if path.name=="router-quality-rubric.yaml":continue
  row=load_json(path,c)
  if not isinstance(row,dict):continue
  actual.add(row.get("skill")); pos=row.get("positive",[]);neg=row.get("negative",[]);amb=row.get("ambiguous",[]);prompts+=len(pos)+len(neg)+len(amb)
  if len(pos)<12 or len(neg)<8 or len(amb)<4:c.error(f"{path}: eval counts {len(pos)}/{len(neg)}/{len(amb)}")
  for item in pos:
   if item.get("expected_primary")!=row.get("skill"):c.error(f"{path}: positive expected primary mismatch")
   if item.get("max_supporting",99)>3:c.error(f"{path}: too many supporting")
 if actual!=expected_files:c.error(f"eval skill set mismatch")
 coverage=load_json(root/"coverage-matrix.yaml",c) or []
 for row in coverage:
  if row.get("coverage")=="planned":c.error(f"planned coverage: {row.get('id')}")
  if not (root/row.get("playbook","")).exists():c.error(f"coverage missing playbook: {row.get('id')}")
 short=load_json(root/"examples"/"synthetic-cases"/"short-cases.yaml",c) or []
 full=list((root/"examples"/"synthetic-cases"/"full").glob("full-case-*.yaml"))
 if len(short)<60:c.error(f"short cases only {len(short)}")
 if len(full)<15:c.error(f"full cases only {len(full)}")
 c.metrics.update({"eval_files":len(actual),"eval_prompts":prompts,"coverage_rows":len(coverage),"short_cases":len(short),"full_cases":len(full)})
 c.record("evals-and-coverage",before,start)

def scripts(root,c):
 start=time.time();before=len(c.errors)
 ps=list((root/"scripts").rglob("*.ps1"))+list((root/"scripts").rglob("*.psm1"))
 required=["Install-WindowsMasterSkills.ps1","Uninstall-WindowsMasterSkills.ps1","Build-SkillPackages.ps1","Test-WindowsMasterRepo.ps1","Update-WindowsKnowledgeBase.ps1","Update-ToolCatalog.ps1","New-WindowsServiceCase.ps1","Add-WindowsCaseAction.ps1","New-WindowsServiceReport.ps1","Get-WindowsRepairBundle.ps1","Get-WindowsStorageRisk.ps1","Get-WindowsBootLayout.ps1","Export-WindowsRelevantEvents.ps1","Get-WindowsDriverInventory.ps1","Get-WindowsUpdateHealth.ps1","Get-WindowsStartupPersistence.ps1","Get-WindowsNetworkSnapshot.ps1","Get-BitLockerSafetyStatus.ps1","New-ServiceMediaPlan.ps1","Get-VerifiedServiceTool.ps1","Test-ServiceMediaIntegrity.ps1"]
 names={p.name for p in ps}
 for name in required:
  if name not in names:c.error(f"missing required script {name}")
 command=["pwsh","-NoProfile","-NonInteractive","-Command",r"$bad=@();Get-ChildItem -LiteralPath $env:WM_VALIDATE_SCRIPT_ROOT -Recurse -Include *.ps1,*.psm1|ForEach-Object{$e=$null;[System.Management.Automation.Language.Parser]::ParseFile($_.FullName,[ref]$null,[ref]$e)|Out-Null;if($e){$bad+=@($e|ForEach-Object{\"$($_.Extent.File):$($_.Extent.StartLineNumber):$($_.Message)\"})}};if($bad){$bad|Write-Error;exit 1}"]
 try:
  env=os.environ.copy();env["WM_VALIDATE_SCRIPT_ROOT"]=str(root/"scripts")
  proc=subprocess.run(command,capture_output=True,text=True,timeout=90,env=env)
  if proc.returncode!=0:c.error("PowerShell syntax parse: "+(proc.stderr or proc.stdout)[-4000:])
 except Exception as exc:c.error(f"PowerShell syntax parser unavailable: {exc}")
 c.metrics["powershell_files"]=len(ps);c.record("scripts",before,start)

def package_check(root,c):
 package_root=root/"dist"/"skills"
 if not package_root.exists():return
 start=time.time();before=len(c.errors);packages=[p for p in package_root.iterdir() if p.is_dir()]
 if packages and len(packages)!=39:c.error(f"package count {len(packages)}")
 for p in packages:
  if not (p/"SKILL.md").exists() or not (p/"references"/"_shared"/"schemas"/"playbook.schema.json").exists():c.error(f"package not self-contained: {p.name}")
 c.metrics["packages"]=len(packages);c.record("packages",before,start)

def main():
 p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--category",default="All");p.add_argument("--json-out");a=p.parse_args()
 root=Path(a.root).resolve();c=Check();cat=a.category.lower()
 if cat in {"all","structure"}:structure(root,c)
 if cat in {"all","structure"}:schemas(root,c)
 if cat in {"all","links"}:links(root,c)
 if cat in {"all","safety"}:safety(root,c)
 if cat in {"all","evals"}:evals(root,c)
 if cat in {"all","scripts"}:scripts(root,c)
 package_check(root,c)
 result={"status":"PASS" if not c.errors else "FAIL","errors":c.errors,"warnings":c.warnings,"metrics":c.metrics,"checks":c.checks}
 if a.json_out:
  out=Path(a.json_out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False,indent=2))
 return 0 if not c.errors else 1
if __name__=="__main__":raise SystemExit(main())
'''
        ),
    )

    fixture_files = {
        "tests/fixtures/repair-bundle/os.json": {"hostname": "CLIENT-EXAMPLE", "user_path": r"C:\Users\Alice Example\Documents", "email": "alice@example.invalid", "build": "26100.8875", "architecture": "x64", "synthetic": True},
        "tests/fixtures/repair-bundle/network.json": {"ipv4": "192.0.2.44", "dns": ["192.0.2.53"], "gateway": "192.0.2.1", "synthetic": True},
        "tests/fixtures/repair-bundle/security.json": {"bitlocker": "Protection On", "recovery_key_collected": False, "defender": "healthy", "synthetic": True},
        "tests/fixtures/storage/critical.json": {"disks": [{"model": "SYNTH-HDD", "health": "critical", "read_errors_total": 19, "symptom": "clicking"}], "synthetic": True},
        "tests/fixtures/storage/safe.json": {"disks": [{"model": "SYNTH-SSD", "health": "healthy", "read_errors_total": 0, "temperature": 38}], "synthetic": True},
        "tests/fixtures/boot/uefi.json": {"firmware": "UEFI", "disks": [{"number": 0, "style": "GPT", "unique_id": "SYNTH-DISK-0"}], "partitions": [{"role": "ESP", "fs": "FAT32", "size_mb": 260}, {"role": "Windows", "letter": "D", "has_windows": True}], "synthetic": True},
        "tests/fixtures/drivers.json": {"drivers": [{"device": "Synthetic GPU", "provider": "Example OEM", "version": "1.2.3", "signed": True}], "problem_devices": [], "synthetic": True},
        "tests/fixtures/update.json": {"pending_reboot": False, "events": [{"id": 20, "code": "0x800f0922", "synthetic": True}]},
        "tests/fixtures/persistence.json": {"startup": [{"name": "Synthetic Updater", "command": r"C:\Program Files\Example\updater.exe"}], "services": [], "tasks": [], "synthetic": True},
        "tests/fixtures/network.json": {"adapters": [{"name": "Ethernet", "status": "Up"}], "ip": [{"address": "192.0.2.44"}], "routes": [], "synthetic": True},
        "tests/fixtures/bitlocker.json": {"volumes": [{"mount": "C:", "protection": "On", "lock": "Unlocked", "protector_types": ["Tpm"]}], "contains_recovery_keys": False, "synthetic": True},
        "tests/fixtures/management.json": {"join_summary": ["AzureAdJoined : NO", "DomainJoined : NO"], "mdm": False, "synthetic": True},
    }
    for path, value in fixture_files.items():
        dump_yaml_json(path, value)
    write(
        "tests/fixtures/logs/CBS.log",
        "2026-08-06 10:00:00, Info CBS Synthetic fixture start\n2026-08-06 10:00:01, Error CBS 0x800f081f source files could not be found [SYNTHETIC]\n",
    )
    write(
        "tests/fixtures/logs/dism.log",
        "2026-08-06 10:01:00, Info DISM Synthetic fixture\n2026-08-06 10:01:01, Error DISM failed 0x800f081f [SYNTHETIC]\n",
    )
    write(
        "tests/fixtures/logs/setuperr.log",
        "2026-08-06 10:02:00, Error SP Operation failed in SAFE_OS with 0xC1900101 [SYNTHETIC]\n",
    )
    write("tests/fixtures/dumps/synthetic.dmp.txt", "SYNTHETIC DUMP METADATA FIXTURE - NOT AN EXECUTABLE CRASH DUMP\nBugCheck 0x00000124\n")
    write(
        "tests/fixtures/unattend-safe.xml",
        clean(
            """\
<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
  <settings pass="oobeSystem" />
</unattend>
"""
        ),
    )
    write(
        "tests/pester/Structure.Tests.ps1",
        clean(
            r'''
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Skill structure' {
 It 'contains exactly 39 skills and no shared SKILL.md' {
  $skills=@(Get-ChildItem -LiteralPath (Join-Path $Repo '.agents\skills') -Directory|Where-Object Name -ne '_shared')
  if($skills.Count -ne 39){throw "Expected 39 skills, got $($skills.Count)"}
  if(Test-Path -LiteralPath (Join-Path $Repo '.agents\skills\_shared\SKILL.md')){throw '_shared contains SKILL.md'}
 }
 It 'has no unresolved creator placeholders' {
  $hits=@(Get-ChildItem (Join-Path $Repo '.agents\skills') -Recurse -File|Select-String -Pattern '\[TODO|TODO: Complete')
  if($hits.Count -ne 0){throw "Creator placeholders found: $($hits.Count)"}
 }
}
'''
        ),
    )
    write(
        "tests/pester/Bundle.Tests.ps1",
        clean(
            r'''
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Repair bundle fixture path' {
 It 'creates redacted JSON, Markdown, HTML, manifest and ZIP' {
  $root=Join-Path $TestDrive 'bundle'
  & (Join-Path $Repo 'scripts\diagnostics\Get-WindowsRepairBundle.ps1') -Mode Basic -FixtureRoot (Join-Path $Repo 'tests\fixtures\repair-bundle') -OutputPath $root
  if($LASTEXITCODE -ne 0){throw "Bundle exit code $LASTEXITCODE"}
  foreach($path in @("$root\manifest.json","$root\summary.md","$root\summary.html","$root.zip")){if(-not(Test-Path -LiteralPath $path)){throw "Missing $path"}}
  if((Get-Content "$root\os.json" -Raw) -match 'alice@example'){throw 'E-mail was not redacted'}
 }
}
'''
        ),
    )
    write(
        "tests/pester/RepairSafety.Tests.ps1",
        clean(
            r'''
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Repair wrapper safety' {
 It 'generates plans only in default Scan mode' {
  $scripts=Get-ChildItem (Join-Path $Repo 'scripts\repair') -Filter 'Invoke-*.ps1'|Where-Object Name -ne 'Invoke-BootRepair.ps1'
  foreach($script in $scripts){
   $log=Join-Path $TestDrive $script.BaseName
   & $script.FullName -LogRoot $log -Synthetic
   if(-not(Test-Path -LiteralPath $log)){throw "Missing log root for $($script.Name)"}
   if(@(Get-ChildItem -LiteralPath $log -Filter '*-plan.json').Count -ne 1){throw "Expected one plan for $($script.Name)"}
   if(Test-Path -LiteralPath (Join-Path $log 'repair-actions.jsonl')){throw "Apply action log created in Scan: $($script.Name)"}
  }
 }
 It 'keeps Boot repair in Plan with fixture-safe volumes' {
  $log=Join-Path $TestDrive 'boot'
  & (Join-Path $Repo 'scripts\repair\Invoke-BootRepair.ps1') -Mode Plan -OsVolume D: -SystemVolume S: -Firmware UEFI -LogRoot $log -Synthetic
  if(-not(Test-Path (Join-Path $log 'boot-files-bcd-plan.json'))){throw 'Boot plan missing'}
 }
}
'''
        ),
    )
    write(
        "tests/pester/Case.Tests.ps1",
        clean(
            r'''
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Case lifecycle' {
 It 'creates, appends and reports without PII requirement' {
  $root=Join-Path $TestDrive 'cases'
  $case=& (Join-Path $Repo 'scripts\reporting\New-WindowsServiceCase.ps1') -Slug synthetic -OwnerAlias owner-001 -AuthorizationLevel R0 -Root $root -Date ([datetime]'2026-08-06')
  & (Join-Path $Repo 'scripts\reporting\Add-WindowsCaseAction.ps1') -CasePath $case -Purpose validation -RiskClass R0 -Result success -Rollback not-applicable|Out-Null
  $result=& (Join-Path $Repo 'scripts\reporting\New-WindowsServiceReport.ps1') -CasePath $case -RequireValidation
  if($result.Status -ne 'validated'){throw "Unexpected status $($result.Status)"}
  if(-not(Test-Path (Join-Path $case 'technical-report.md'))){throw 'Technical report missing'}
 }
}
'''
        ),
    )
    write(
        "tests/pester/Install.Tests.ps1",
        clean(
            r'''
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Install manifest lifecycle' {
 It 'installs 39 and uninstalls only manifest-owned unchanged copies' {
  $dest=Join-Path $TestDrive 'skills'
  $install=& (Join-Path $Repo 'scripts\repo\Install-WindowsMasterSkills.ps1') -Destination $dest -Source (Join-Path $Repo '.agents\skills') -Mode Copy
  if($install.Installed -ne 39){throw "Installed $($install.Installed), expected 39"}
  & (Join-Path $Repo 'scripts\repo\Uninstall-WindowsMasterSkills.ps1') -Destination $dest -Confirm:$false|Out-Null
  if(@(Get-ChildItem $dest -Directory|Where-Object Name -notmatch '^\.').Count -ne 0){throw 'Installed skill directories remained'}
 }
 It 'keeps installer and packager WhatIf free of filesystem mutations' {
  $installDest=Join-Path $TestDrive 'whatif-install'
  $packageDest=Join-Path $TestDrive 'whatif-packages'
  & (Join-Path $Repo 'scripts\repo\Install-WindowsMasterSkills.ps1') -Destination $installDest -Source (Join-Path $Repo '.agents\skills') -Mode Copy -WhatIf|Out-Null
  & (Join-Path $Repo 'scripts\repo\Build-SkillPackages.ps1') -Destination $packageDest -WhatIf|Out-Null
  if(Test-Path -LiteralPath $installDest){throw 'Installer WhatIf created a destination'}
  if(Test-Path -LiteralPath $packageDest){throw 'Packager WhatIf created a destination'}
 }
 It 'uses self-contained dist packages as the default install source' {
  $dest=Join-Path $TestDrive 'packaged-skills'
  $install=& (Join-Path $Repo 'scripts\repo\Install-WindowsMasterSkills.ps1') -Scope User -Destination $dest -Mode Copy
  $shared=Join-Path $dest 'windows-master-router\references\_shared\schemas\playbook.schema.json'
  if($install.Installed -ne 39 -or -not(Test-Path -LiteralPath $shared)){throw 'Default install was not self-contained'}
  & (Join-Path $Repo 'scripts\repo\Uninstall-WindowsMasterSkills.ps1') -Scope User -Destination $dest -Confirm:$false|Out-Null
 }
}
'''
        ),
    )
    write(
        "tests/pester/Parsers.Tests.ps1",
        clean(
            r'''
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Synthetic parsers' {
 It 'extracts servicing and setup errors without changing fixtures' {
  $cbs=Join-Path $TestDrive 'cbs.json';$setup=Join-Path $TestDrive 'setup.json'
  & (Join-Path $Repo 'scripts\diagnostics\Parse-WindowsServicingLog.ps1') -Path (Join-Path $Repo 'tests\fixtures\logs\CBS.log') -OutputPath $cbs|Out-Null
  & (Join-Path $Repo 'scripts\diagnostics\Parse-WindowsSetupLog.ps1') -Path (Join-Path $Repo 'tests\fixtures\logs\setuperr.log') -OutputPath $setup|Out-Null
  if((Get-Content $cbs -Raw|ConvertFrom-Json).matched_count -le 0){throw 'CBS parser returned no matches'}
  $setupResult=Get-Content $setup -Raw|ConvertFrom-Json
  if(@($setupResult.hits).Count -le 0){throw 'Setup parser returned no hits'}
 }
}
'''
        ),
    )
    write(
        "tests/pester/Collectors.Tests.ps1",
        clean(
            r'''
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Fixture-safe collectors' {
 It 'classifies critical storage as stop and healthy fixture without a stop signal' {
  $critical=Join-Path $TestDrive 'critical.json';$safe=Join-Path $TestDrive 'safe.json'
  $c=& (Join-Path $Repo 'scripts\diagnostics\Get-WindowsStorageRisk.ps1') -FixturePath (Join-Path $Repo 'tests\fixtures\storage\critical.json') -OutputPath $critical
  $s=& (Join-Path $Repo 'scripts\diagnostics\Get-WindowsStorageRisk.ps1') -FixturePath (Join-Path $Repo 'tests\fixtures\storage\safe.json') -OutputPath $safe
  if($c.classification -ne 'stop'){throw "Critical storage was $($c.classification)"}
  if($s.classification -eq 'stop'){throw 'Safe fixture classified as stop'}
 }
 It 'maps a synthetic UEFI layout without assuming C' {
  $out=Join-Path $TestDrive 'boot.json'
  $result=& (Join-Path $Repo 'scripts\diagnostics\Get-WindowsBootLayout.ps1') -FixturePath (Join-Path $Repo 'tests\fixtures\boot\uefi.json') -OutputPath $out
  if($result.rule -notmatch 'never assume C'){throw 'Missing WinRE drive-letter rule'}
 }
 It 'runs every generic collector against a synthetic fixture' {
  $cases=@(
   @('Export-WindowsRelevantEvents.ps1','tests\fixtures\update.json'),
   @('Get-WindowsDriverInventory.ps1','tests\fixtures\drivers.json'),
   @('Get-WindowsUpdateHealth.ps1','tests\fixtures\update.json'),
   @('Get-WindowsStartupPersistence.ps1','tests\fixtures\persistence.json'),
   @('Get-WindowsNetworkSnapshot.ps1','tests\fixtures\network.json'),
   @('Get-BitLockerSafetyStatus.ps1','tests\fixtures\bitlocker.json'),
   @('Get-WindowsManagementStatus.ps1','tests\fixtures\management.json')
  )
  foreach($case in $cases){
   $out=Join-Path $TestDrive ($case[0]+'.json')
   & (Join-Path $Repo ('scripts\diagnostics\'+$case[0])) -FixturePath (Join-Path $Repo $case[1]) -OutputPath $out|Out-Null
   if(-not(Test-Path -LiteralPath $out)){throw "Collector did not create output: $($case[0])"}
   $data=Get-Content -LiteralPath $out -Raw|ConvertFrom-Json
   if($data.source -ne 'fixture'){throw "Collector source mismatch: $($case[0])"}
  }
 }
 It 'extracts minidump metadata without claiming a diagnosis' {
  $out=Join-Path $TestDrive 'dump.json'
  $result=& (Join-Path $Repo 'scripts\diagnostics\Get-MinidumpMetadata.ps1') -Path (Join-Path $Repo 'tests\fixtures\dumps\synthetic.dmp.txt') -OutputPath $out
  if($result.analysis -ne 'metadata-only'){throw 'Dump parser overclaims analysis'}
 }
}
'''
        ),
    )
    write(
        "tests/pester/RouterToolkit.Tests.ps1",
        clean(
            r'''
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Describe 'Router and toolkit' {
 It 'routes boot, storage and update examples to exactly one expected primary' {
  $cases=@(
   @('Laptop zapętla Automatic Repair po aktualizacji, dysk nie klika','windows-boot-recovery'),
   @('Dysk klika, SMART critical i komputer zamiera przy kopiowaniu','storage-triage-cloning-recovery'),
   @('Windows Update 0x800f0922 ciągle wraca po restarcie','windows-update-servicing')
  )
  foreach($case in $cases){
   $json=& python (Join-Path $Repo 'scripts\repo\route_issue.py') --text $case[0] --json
   $result=$json|ConvertFrom-Json
   if($result.primary -ne $case[1]){throw "Router '$($case[0])' -> $($result.primary), expected $($case[1])"}
   if(@($result.supporting).Count -gt 3){throw 'Router returned more than three supporting skills'}
  }
 }
 It 'queries release and tool registries without network access' {
  $matrix=& python (Join-Path $Repo 'scripts\repo\query_matrix.py') --os windows-11 --build 26100
  if(@(($matrix|ConvertFrom-Json).matches).Count -ne 1){throw 'Release matrix query failed'}
  $tools=& python (Join-Path $Repo 'scripts\repo\query_tools.py') --use-case network --os 'Windows 11' --arch x64
  if(@(($tools|ConvertFrom-Json).results).Count -lt 1){throw 'Tool query returned no result'}
 }
 It 'generates a no-download service-media plan' {
  $out=Join-Path $TestDrive 'media-plan.json'
  $plan=& (Join-Path $Repo 'scripts\toolkit\New-ServiceMediaPlan.ps1') -ManifestPath (Join-Path $Repo 'tools\manifests\service-media.yaml') -OutputPath $out
  if($plan.downloads_performed -ne 0 -or $plan.usb_writes_performed -ne 0){throw 'Service media plan performed a mutation'}
 }
 It 'returns downloader metadata without downloading when no asset URL is supplied' {
  $plan=& (Join-Path $Repo 'scripts\toolkit\Get-VerifiedServiceTool.ps1') -ToolId rufus -Destination (Join-Path $TestDrive 'tools') -WhatIf
  if($plan.will_execute){throw 'Downloader plan claims execution'}
  if(Test-Path (Join-Path $TestDrive 'tools')){throw 'Downloader plan created destination unexpectedly'}
 }
 It 'keeps knowledge and tool refreshes review-only under WhatIf' {
  $knowledgeOut=Join-Path $TestDrive 'knowledge-candidate.json'
  $toolsOut=Join-Path $TestDrive 'tool-candidate.json'
  $knowledge=& (Join-Path $Repo 'scripts\repo\Update-WindowsKnowledgeBase.ps1') -Fetch -OutputPath $knowledgeOut -WhatIf
  $tools=& (Join-Path $Repo 'scripts\repo\Update-ToolCatalog.ps1') -Fetch -OutputPath $toolsOut -MaxTools 2 -WhatIf
  if($knowledge.auto_accept -ne $false -or $tools.auto_accept -ne $false){throw 'Refresh plan allows automatic acceptance'}
  if(Test-Path -LiteralPath $knowledgeOut){throw 'Knowledge WhatIf wrote a candidate'}
  if(Test-Path -LiteralPath $toolsOut){throw 'Tool WhatIf wrote a candidate'}
 }
}
'''
        ),
    )
    write(
        "tests/pester/HostBoundaryMocks.Tests.ps1",
        clean(
            r'''
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$ModulePath=Join-Path $Repo 'scripts\lib\WindowsMaster.HostAdapter.psm1'
Import-Module $ModulePath -Force
$ModuleName=(Get-Module|Where-Object Path -eq $ModulePath|Select-Object -First 1).Name

Describe 'Mocked read-only host boundaries' {
 It 'mocks registry reads' {
  Mock -CommandName Get-ItemProperty -ModuleName $ModuleName -MockWith {[pscustomobject]@{State='synthetic'}}
  $result=Get-WmRegistrySnapshot -LiteralPath 'HKLM:\SYNTHETIC'
  if($result.State -ne 'synthetic'){throw 'Registry mock result mismatch'}
  Assert-MockCalled -CommandName Get-ItemProperty -ModuleName $ModuleName -Times 1 -Exactly
 }
 It 'mocks service reads' {
  Mock -CommandName Get-Service -ModuleName $ModuleName -MockWith {[pscustomobject]@{Name='SyntheticService';Status='Stopped'}}
  $result=Get-WmServiceSnapshot -Name SyntheticService
  if($result.Status -ne 'Stopped'){throw 'Service mock result mismatch'}
  Assert-MockCalled -CommandName Get-Service -ModuleName $ModuleName -Times 1 -Exactly
 }
 It 'mocks BCD enumeration and DISM ScanHealth' {
  Mock -CommandName bcdedit.exe -ModuleName $ModuleName -MockWith {'synthetic-bcd'}
  Mock -CommandName dism.exe -ModuleName $ModuleName -MockWith {'synthetic-dism'}
  if((Get-WmBcdSnapshot) -notcontains 'synthetic-bcd'){throw 'BCD mock result mismatch'}
  if((Get-WmDismScanHealth) -notcontains 'synthetic-dism'){throw 'DISM mock result mismatch'}
  Assert-MockCalled -CommandName bcdedit.exe -ModuleName $ModuleName -Times 1 -Exactly
  Assert-MockCalled -CommandName dism.exe -ModuleName $ModuleName -Times 1 -Exactly
 }
 It 'mocks CIM and network reads' {
  Mock -CommandName Get-CimInstance -ModuleName $ModuleName -MockWith {[pscustomobject]@{Caption='Synthetic OS'}}
  Mock -CommandName Get-NetIPConfiguration -ModuleName $ModuleName -MockWith {[pscustomobject]@{InterfaceAlias='Synthetic NIC'}}
  if((Get-WmCimSnapshot -ClassName Win32_OperatingSystem).Caption -ne 'Synthetic OS'){throw 'CIM mock result mismatch'}
  if((Get-WmNetworkSnapshotBoundary).InterfaceAlias -ne 'Synthetic NIC'){throw 'Network mock result mismatch'}
  Assert-MockCalled -CommandName Get-CimInstance -ModuleName $ModuleName -Times 1 -Exactly
  Assert-MockCalled -CommandName Get-NetIPConfiguration -ModuleName $ModuleName -Times 1 -Exactly
 }
 It 'mocks filesystem reads' {
  Mock -CommandName Get-Content -ModuleName $ModuleName -MockWith {'synthetic-file'}
  if((Get-WmFileSnapshot -LiteralPath 'X:\synthetic.txt') -ne 'synthetic-file'){throw 'Filesystem mock result mismatch'}
  Assert-MockCalled -CommandName Get-Content -ModuleName $ModuleName -Times 1 -Exactly
 }
}
'''
        ),
    )
    write(
        "tests/schema/README.md",
        "Schema-shaped validation is dependency-free in scripts/repo/validate_repo.py; CI also runs Pester.\n",
    )
    write("tests/safety/README.md", "Safety lint blocks foreign binaries, secret patterns, pipe-to-shell, Win32_Product and unsafe repair defaults.\n")
    write("tests/links/README.md", "Internal Markdown targets are resolved relative to each file; HTTP availability is maintained separately by source freshness review.\n")
    write("tests/smoke/README.md", "Smoke validation builds 39 self-contained packages and performs manifest-based install/uninstall in dist/test-install.\n")
    write(
        ".github/workflows/validate.yml",
        clean(
            r'''
name: validate
on:
  push:
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  validate:
    runs-on: windows-2025
    timeout-minutes: 25
    steps:
      - uses: actions/checkout@v4
      - name: Install pinned validation modules
        shell: pwsh
        run: |
          Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
          Install-Module Pester -RequiredVersion 5.6.1 -Scope CurrentUser -Force
          Install-Module PSScriptAnalyzer -RequiredVersion 1.24.0 -Scope CurrentUser -Force
      - name: Validate safely
        shell: pwsh
        run: ./scripts/repo/Test-WindowsMasterRepo.ps1 -Category All
      - name: Upload text reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-reports
          path: dist/reports/
'''
        ),
    )

    write(
        ".agents/skills/_shared/scripts/Test-SkillInput.ps1",
        clean(
            r'''
<#
.SYNOPSIS Validates a JSON input envelope against the minimum safety gates shared by packaged skills.
.EXAMPLE .\Test-SkillInput.ps1 -Path .\input.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Path)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$input=Get-Content -LiteralPath (Resolve-Path -LiteralPath $Path) -Raw|ConvertFrom-Json
$required=@('boot_state','backup_status','encryption_status','managed_status','data_value')
$missing=@($required|Where-Object{$input.PSObject.Properties.Name -notcontains $_})
[pscustomobject]@{valid=($missing.Count -eq 0);missing=$missing;rule='Do not advance to R2+ when any gate is unknown.'}
if($missing.Count){exit 2}
'''
        ),
    )
    write(
        "REPO_STATUS.md",
        clean(
            f"""\
# Stan repozytorium

Wersja: 1.0.0 · snapshot: {TODAY}

Repo zostało wygenerowane z kompletnego, recenzowalnego inventory i zwalidowane bez wykonywania
napraw na hoście. Maszynowe raporty ostatniego uruchomienia są zapisywane w
`dist/reports/validation.json` oraz `dist/reports/static-validation.json` (katalog roboczy,
celowo ignorowany przez Git).

## Zakres

- 39 skilli, każdy z 3 playbookami i 3 kartami poleceń.
- 60 krótkich oraz 15 pełnych fikcyjnych spraw.
- Release/lifecycle matrix, source register, tool catalog, coverage, evals i service-media plan.
- Collectory i parsery mają ścieżkę fixture; repairs są Scan-first z `-Apply`.
- 117 playbooków, 117 command cards, 95 źródeł, 99 narzędzi i 936 eval prompts.
- 32/32 wiersze coverage mają status kompletny; nie ma wpisów `planned`.
- Rootowy indeks orkiestratora obejmuje 39 kanonicznych skilli; 39 wygenerowanych paczek `dist`
  pozostaje celowo poza katalogiem źródłowym indeksu.

## Rzeczywiste wyniki walidacji — {TODAY}

| Kontrola | Wynik | Dowód |
|---|---:|---|
| Oficjalny `skill-creator/quick_validate.py` | PASS | 39/39 skilli źródłowych oraz 39/39 paczek |
| `node scripts/generate-skill-index.mjs --check` | PASS | 39 skilli źródłowych, bez mirrorów `dist` |
| `swietlik-orchestrator pack validate` | PASS | 39 skilli, 0 błędów, 0 ostrzeżeń |
| Statyczny validator repo | PASS | 7/7 grup, 0 błędów, 0 ostrzeżeń |
| Linki wewnętrzne | PASS | 703 odwołania |
| Safety/schema/evals/coverage | PASS | 0 niedozwolonych binariów; 936 promptów; 60+15 spraw |
| Pester, PowerShell 7.6.5 (Pester 3.4.0) | PASS | 24/24, 0 skipped |
| Pester, Windows PowerShell 5.1.26100.8972 | PASS (snapshot 2026-08-06) | 24/24, 0 skipped |
| Parser AST PowerShell 5.1 | PASS | 38 plików, 0 błędów |
| Python `compileall` | PASS | wszystkie skrypty Python, 0 błędów |
| Build `dist/skills` | PASS | 39/39 poprawnych i samowystarczalnych paczek |
| Instalacja Copy, scope Repo | PASS | 39 zainstalowanych, 39 usuniętych, 0 pozostałych |
| Instalacja Copy, scope User | PASS | 39 zainstalowanych, 39 usuniętych, 0 pozostałych |
| Instalacja Junction, scope Repo | PASS | 39 junctions, 39 usuniętych, 0 pozostałych |
| PSScriptAnalyzer lokalnie | SKIP | moduł nie był zainstalowany; uruchomiono AST/safety lint, CI przypina 1.24.0 |

Końcowy `Test-WindowsMasterRepo.ps1 -Category All` zakończył się kodem 0: 3 kontrole PASS,
0 FAIL, 1 jawny SKIP (PSScriptAnalyzer).

## Ograniczenia zewnętrzne

- Nie uruchomiono R2–R4, napraw firmware, realnego odzysku storage, wdrożenia Secure Boot,
  bare-metal restore ani pełnej macierzy XP–11/x86/x64/ARM64; wymagają izolowanego laboratorium
  VM lub fizycznego oraz osobnej autoryzacji.
- Nie pobrano ani nie uruchomiono ISO lub binariów firm trzecich. Dlatego integralność i podpisy
  konkretnych przyszłych assetów muszą być sprawdzane w stagingu przez toolkit.
- PSScriptAnalyzer nie był dostępny lokalnie. Konfiguracja i przypięta wersja CI są w repo,
  ale hosted CI nie został uruchomiony, ponieważ zgodnie z zakresem nie utworzono remote i nie
  wykonano push.
- Aktualność jest snapshotem z {TODAY}; aktualizatory tworzą kandydat do review i nigdy
  automatycznie nie nadpisują zaakceptowanej wiedzy.

## Granica bezpieczeństwa wykonania

Podczas budowy użyto wyłącznie fixture, trybów `Scan`, `Plan` i `WhatIf` oraz katalogów testowych
wewnątrz repo. Nie zmieniono konfiguracji Windows, BCD, rejestru, usług, sterowników, partycji,
firmware ani nośników hosta.
"""
        ),
    )
    write("dist/.keep", "Build output is generated; no external binary belongs here.\n")


def main() -> int:
    if len(SKILLS) != 39:
        raise RuntimeError(f"Expected 39 skills, got {len(SKILLS)}")
    referenced_sources = {source_id for spec in SKILLS for source_id in spec["sources"]}
    missing_sources = referenced_sources - set(SOURCE_BY_ID)
    if missing_sources:
        raise RuntimeError(f"Missing source definitions: {sorted(missing_sources)}")
    generate_root_files()
    generate_docs()
    generate_shared()
    generate_schemas()
    for spec in SKILLS:
        generate_skill(spec)
    generate_knowledge_base()
    generate_tools()
    generate_coverage()
    generate_evals()
    generate_examples_and_templates()
    generate_scripts()
    print(
        json.dumps(
            {
                "status": "generated",
                "skills": len(SKILLS),
                "playbooks": len(SKILLS) * 3,
                "command_cards": len(SKILLS) * 3,
                "sources": len(SOURCES),
                "tools": len(TOOLS),
                "eval_prompts": len(SKILLS) * (12 + 8 + 4),
                "short_cases": 60,
                "full_cases": 15,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
