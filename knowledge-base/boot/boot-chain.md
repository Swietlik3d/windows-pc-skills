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
