# windows-master-service-skills

Prywatny, polskojęzyczny „drugi mózg” serwisanta Windows XP–11. Repo prowadzi od intake,
ochrony danych i dowodów przez różnicowanie hipotez do kontrolowanej naprawy, rollbacku,
walidacji i raportu. Nie jest zestawem magicznych one-linerów, nie obchodzi haseł/BitLocker,
nie zawiera ISO, driverów ani cudzych binariów i nie uruchamia napraw samoczynnie.

Snapshot wiedzy zależnej od wersji: **2026-08-06**. Przed użyciem informacji starszej niż 90 dni
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
& .\scripts\repo\Test-WindowsMasterRepo.ps1 -Category All
```

Instalacja repo-local (domyślne źródło `.agents/skills`, bez instalowania `_shared` jako skilla):

```powershell
& .\scripts\repo\Install-WindowsMasterSkills.ps1 -Scope Repo -Mode Copy
```

Instalacja user-wide do `$HOME/.agents/skills`:

```powershell
& .\scripts\repo\Install-WindowsMasterSkills.ps1 -Scope User -Mode Copy
```

Jawne wywołanie: `$windows-update-servicing Zdiagnozuj 0x800f0922, najpierw tylko R0`.
Szerokie zgłoszenie: `$windows-master-router Laptop zapętla Automatic Repair po aktualizacji`.

Bundle na fixture (bez dotykania hosta):

```powershell
& .\scripts\diagnostics\Get-WindowsRepairBundle.ps1 -Mode Basic `
  -FixtureRoot .\tests\fixtures\repair-bundle -OutputPath .\dist\sample-bundle
```

Nowa syntetyczna sprawa i raport:

```powershell
& .\scripts\reporting\New-WindowsServiceCase.ps1 -Slug update-loop `
  -OwnerAlias customer-001 -AuthorizationLevel R0 -Root .\dist\cases
& .\scripts\reporting\New-WindowsServiceReport.ps1 `
  -CasePath .\dist\cases\2026-08-06-update-loop
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
& .\scripts\repo\Build-SkillPackages.ps1
& .\scripts\repo\Uninstall-WindowsMasterSkills.ps1 -Scope User -RestoreBackup
```

Można też wskazać `-Destination <TEMP>` do bezpiecznego testu. User scope według aktualnej
oficjalnej dokumentacji Codex to `$HOME/.agents/skills`.

## Aktualizacja wiedzy i narzędzi

Updatery tworzą tylko kandydat/diff; nigdy automatycznie nie uznają sieciowej odpowiedzi za
prawdę:

```powershell
& .\scripts\repo\Update-WindowsKnowledgeBase.ps1 -WhatIf
& .\scripts\repo\Update-ToolCatalog.ps1 -WhatIf
```

Kolejność zaufania: Microsoft → OEM/vendor → oficjalny projekt → moderowana społeczność →
agregator tylko jako trop. Katalog zapisuje licencję, commercial use, redistribution, wersję,
official source i metodę integralności.

## Prywatność i licencje

`cases/`, dumpy, bundle i dane klienta są ignorowane przez Git. Collectory redagują username,
hostname, e-mail i adresy domyślnie; nie zbierają haseł, cookies, tokenów, pełnych product keys
ani recovery keys. Kod repo jest prywatny; narzędzia zewnętrzne zachowują własne licencje.

## Mapa 39 skilli

- [`windows-master-router`](.agents/skills/windows-master-router/SKILL.md) — rozpoznanie objawu, ryzyka i wybór dokładnie jednego skilla głównego oraz najwyżej trzech pomocniczych.
- [`windows-service-intake`](.agents/skills/windows-service-intake/SKILL.md) — udokumentowanie właściciela, autoryzacji, wartości danych, szyfrowania, zarządzania, symptomów i zakresu zgody przed serwisem.
- [`windows-case-evidence`](.agents/skills/windows-case-evidence/SKILL.md) — prowadzenie timeline, lekkiego chain of custody, hashy, anonimizacji, artefaktów before/after i raportu serwisowego.
- [`pc-hardware-diagnostics`](.agents/skills/pc-hardware-diagnostics/SKILL.md) — różnicowanie braku zasilania, POST, kodów LED/beep, baterii, ładowania, PSU, płyty i peryferiów bez pracy pod napięciem.
- [`bios-uefi-firmware`](.agents/skills/bios-uefi-firmware/SKILL.md) — bezpieczna identyfikacja ustawień firmware, boot mode, CSM, Secure Boot, TPM oraz aktualizacji i rollbacku po dokładnym modelu.
- [`storage-triage-cloning-recovery`](.agents/skills/storage-triage-cloning-recovery/SKILL.md) — ochrona danych na HDD/SSD/NVMe/USB, SMART, imaging, ddrescue/OpenSuperClone, recovery logiczne i bezwzględna kontrola kierunku zapisu.
- [`memory-cpu-gpu-thermal`](.agents/skills/memory-cpu-gpu-thermal/SKILL.md) — różnicowanie błędów RAM/IMC, WHEA, GPU/VRAM, throttlingu, chłodzenia oraz wpływu OC/UV/XMP/EXPO.
- [`windows-os-identification`](.agents/skills/windows-os-identification/SKILL.md) — ustalenie edition, build, kanału, architektury, języka, boot mode, partycji, WinRE i statusu wsparcia przed doborem poleceń.
- [`windows-boot-recovery`](.agents/skills/windows-boot-recovery/SKILL.md) — diagnozę etapów boot, Automatic Repair loop, Safe Mode, czarnego ekranu, restartów i SrtTrail bez ślepej przebudowy BCD.
- [`winpe-offline-repair`](.agents/skills/winpe-offline-repair/SKILL.md) — identyfikację woluminów, montowanie hive, offline log collection, DISM/SFC i kopiowanie danych w WinRE/WinPE.
- [`windows-bcd-partition-repair`](.agents/skills/windows-bcd-partition-repair/SKILL.md) — kontrolowaną diagnozę i naprawę BCD/BCDBoot/ESP/MBR/GPT/NVRAM po pełnej identyfikacji celu.
- [`windows-component-repair`](.agents/skills/windows-component-repair/SKILL.md) — diagnozę CBS/component store oraz dopasowanie źródła WIM/ESD przed SFC/DISM online i offline.
- [`windows-update-servicing`](.agents/skills/windows-update-servicing/SKILL.md) — diagnozę update history, policy, pending reboot, cache, servicing stack i kontrolowany reset komponentów.
- [`windows-setup-upgrade-rollback`](.agents/skills/windows-setup-upgrade-rollback/SKILL.md) — analizę in-place setup, feature update, compatibility blocks, SetupDiag, Panther/Rollback i kontrolowany rollback.
- [`windows-activation-licensing`](.agents/skills/windows-activation-licensing/SKILL.md) — legalną diagnostykę digital license, OEM OA3, edition mismatch i kanałów retail/OEM/volume bez ujawniania kluczy.
- [`windows-bsod-debugging`](.agents/skills/windows-bsod-debugging/SKILL.md) — konfigurację dumpów, analizę bugcheck/stacks/modules/WHEA i ostrożne użycie Driver Verifier z planem odzyskania.
- [`windows-performance-hangs`](.agents/skills/windows-performance-hangs/SKILL.md) — korelację opóźnień, hangów, stutter, CPU/RAM/dysk/GPU, DPC/ISR przy użyciu WPR/WPA, PerfMon i Reliability.
- [`windows-process-service-startup`](.agents/skills/windows-process-service-startup/SKILL.md) — diagnozę procesów, usług, Scheduled Tasks, Autoruns/ProcMon i odwracalny clean boot bez utraty konfiguracji.
- [`windows-drivers-devices`](.agents/skills/windows-drivers-devices/SKILL.md) — diagnozę Device Manager, PnPUtil, Driver Store, SetupAPI, DCH, Code 10/28/31/43 i kontrolowany rollback/offline driver.
- [`windows-network-repair`](.agents/skills/windows-network-repair/SKILL.md) — warstwową diagnozę Ethernet/Wi-Fi/DHCP/DNS/proxy/VPN/routing/firewall/SMB i kontrolowane resety stosu.
- [`windows-peripherals-repair`](.agents/skills/windows-peripherals-repair/SKILL.md) — diagnozę drukarek, spoolera, skanerów, audio, monitorów, USB, Bluetooth, kamer, docków i HID.
- [`windows-accounts-profiles`](.agents/skills/windows-accounts-profiles/SKILL.md) — oficjalne odzyskanie logowania lokalnego/MSA/Entra/Hello oraz naprawę temporary/corrupt profile bez obchodzenia haseł.
- [`windows-ntfs-permissions-shares`](.agents/skills/windows-ntfs-permissions-shares/SKILL.md) — precyzyjną diagnozę ownership, dziedziczenia, effective access, share ACL, offline ACL i świadomość EFS.
- [`windows-bitlocker-tpm-security`](.agents/skills/windows-bitlocker-tpm-security/SKILL.md) — diagnozę Device Encryption/BitLocker, recovery readiness, TPM, Secure Boot, VBS/HVCI, certyfikatów i policy bez obchodzenia ochrony.
- [`windows-malware-remediation`](.agents/skills/windows-malware-remediation/SKILL.md) — izolację, zachowanie dowodów, Defender Offline/MSERT/Sysinternals, PUP/browser hijack, persistence i kryteria reinstalacji.
- [`windows-apps-store-winget`](.agents/skills/windows-apps-store-winget/SKILL.md) — diagnozę instalacji/odinstalowania MSI, ClickOnce, MSIX/AppX, Store, dependencies i winget bez registry cleanerów.
- [`windows-shell-ui-repair`](.agents/skills/windows-shell-ui-repair/SKILL.md) — diagnozę Explorer, Start, Search, Settings, taskbar, shell extensions, ikon i file associations.
- [`windows-office-cloud-repair`](.agents/skills/windows-office-cloud-repair/SKILL.md) — ochronę danych oraz diagnozę Click-to-Run, profili Outlook, PST/OST, OneDrive/Teams sign-in i synchronizacji.
- [`windows-backup-vss-restore`](.agents/skills/windows-backup-vss-restore/SKILL.md) — diagnozę VSS, restore points, File History, Windows Backup, obrazów bare-metal i walidację kopii.
- [`windows-remote-managed-client`](.agents/skills/windows-remote-managed-client/SKILL.md) — transparentną Quick Assist/RDP pomoc oraz wykrycie domain/Entra/MDM, GPO, certyfikatów, mapped drives i firmowych VPN bez łamania zarządzania.
- [`windows-advanced-administration`](.agents/skills/windows-advanced-administration/SKILL.md) — bezpieczną pracę z Event Viewer, registry, services, tasks, local policy, firewall, certyfikaty, storage, SMB, Hyper-V, WSL, Sandbox i power.
- [`windows-automation-powershell`](.agents/skills/windows-automation-powershell/SKILL.md) — projektowanie bezpiecznych, idempotentnych skryptów PowerShell 5.1/7, CIM, remoting, logging, ShouldProcess i testów.
- [`windows-deployment-imaging`](.agents/skills/windows-deployment-imaging/SKILL.md) — planowanie DISM imaging, unattend, Sysprep, ADK/WinPE, drivers offline i migracji HDD→SSD bez ryzyka pomylenia celu.
- [`windows-service-media`](.agents/skills/windows-service-media/SKILL.md) — projekt oficjalnego WinPE lub multiboot USB z manifestem, licencjami, SHA-256/signature i rozdzieleniem x64/ARM64.
- [`windows-legacy-xp-vista-7-8`](.agents/skills/windows-legacy-xp-vista-7-8/SKILL.md) — izolowaną diagnozę legacy BIOS/MBR, NTLDR/boot.ini, starych BCD/WinRE, TLS/certyfikatów, sterowników i migracji.
- [`windows-10-support`](.agents/skills/windows-10-support/SKILL.md) — dynamiczne ustalenie statusu 22H2/ESU/LTSC, bezpieczne utrzymanie i migrację urządzeń pozostających na Windows 10.
- [`windows-11-support`](.agents/skills/windows-11-support/SKILL.md) — obsługę aktywnych gałęzi Windows 11, ARM64, UEFI/GPT, Device Encryption, VBS/HVCI, Hello, DCH i safeguard holds.
- [`windows-post-repair-validation`](.agents/skills/windows-post-repair-validation/SKILL.md) — mierzalne testy przyczyny, objawu i regresji: boot, SMART, temperatury, sleep/wake, update, sieć, peryferia, backup i ryzyko resztkowe.
- [`windows-tool-research`](.agents/skills/windows-tool-research/SKILL.md) — utrzymanie katalogu narzędzi, official sources, wersji, licencji, statusu active/stale/EOL, checksum/signature i community findings.

## Stan i ograniczenia

Zobacz [REPO_STATUS.md](REPO_STATUS.md), [coverage-matrix.yaml](coverage-matrix.yaml),
[snapshot](docs/current-state-snapshot.md) i [kolejkę researchu](RESEARCH_QUEUE.md).
