# Zgodność: Explorer, Start, Search i interfejs

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

W tej domenie szczególnie zweryfikuj: scope user/system, Reliability/WER, shell extension list, AppX events, profile comparison, policy.
