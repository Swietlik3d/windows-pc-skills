# Nośnik serwisowy

Repo projektuje staging, nie zapisuje USB i nie pobiera obrazów. `New-ServiceMediaPlan.ps1`
tworzy plan dla oficjalnego WinPE, jeżeli wykryto ADK i add-on, albo wariantu multiboot.
Aktualny snapshot wskazuje ADK 10.1.28000.1 i konieczność bieżącej poprawki bezpieczeństwa;
przed budową zawsze odśwież źródło.

Układ: `boot/`, `iso/official/`, `linux-rescue/`, `tools/{x64,arm64}`, `drivers/{storage,network}/{x64,arm64}`,
`scripts/`, `docs/`, `cases-encrypted/`, `manifests/`. Dane spraw są szyfrowane oddzielnie.
Każdy asset ma provenance, license, redistribution, exact version, size, SHA-256 oraz
Authenticode/PGP, jeśli wydawca publikuje. R4 write-to-USB wymaga potwierdzenia UniqueId.
