# TPM

Karta współdzielona przez `windows-bitlocker-tpm-security`. Aktualna treść:

## tpm

- **ID:** `windows-bitlocker-tpm-security-cmd-02`
- **Kontekst:** Windows — PowerShell jako administrator
- **Składnia:** `Get-Tpm | Select-Object TpmPresent,TpmReady,TpmEnabled,TpmActivated,AutoProvisioning`
- **Uprawnienia:** zgodnie z opisem kontekstu; nie podnoś ich bez potrzeby.
- **Środowisko:** ustal online/WinRE/WinPE/offline przed uruchomieniem.
- **Zgodność:** sprawdź [compatibility.md](../../.agents/skills/windows-bitlocker-tpm-security/references/compatibility.md); placeholdery muszą być rozwinięte.
- **Działanie:** zbiera lub planuje wyłącznie dane wskazane w nazwie karty.
- **Ryzyko:** `R0`. Dla R2+ wymagaj backupu, jawnego celu, `-Apply` i `ShouldProcess`.
- **Oczekiwany wynik:** Stan TPM bez clear/initialize.
- **Interpretacja błędu:** brak danych lub exit non-zero oznacza `inconclusive`; zachowaj stderr.
- **Rollback:** Brak zmian.
- **Logi:** zapisz stdout/stderr i hash powstałego pliku w sprawie.
- **Bezpieczny przykład:** zamień każdy `<PLACEHOLDER>` na zweryfikowaną wartość i najpierw użyj
  `-WhatIf`, `Scan` lub odpowiednika read-only.
- **Antyprzykład:** uruchomienie na domyślnym `C:` albo nieustalonym dysku jest zabronione.
- **Źródła:** `ms-bitlocker-overview`, `ms-tpm`, `ms-secure-boot-2026`; zweryfikowano 2026-08-06.
