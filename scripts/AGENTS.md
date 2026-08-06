# Instrukcje dla skryptów

- PowerShell 5.1 jest bazą; używaj StrictMode, pełnych nazw cmdletów, try/catch/finally i
  comment-based help.
- Collector ma redakcję domyślną i tryb fixture. Repair domyślnie `Scan`, wymaga `-Apply` oraz
  `SupportsShouldProcess`; nigdy nie wykonuj go na hoście deweloperskim.
- Nie używaj `Invoke-Expression`, pipe-to-shell, Win32_Product ani download-and-run.
- Target path/volume/disk musi być jawny i zweryfikowany. Logi JSONL nie zawierają sekretów.
- Każda nowa funkcja wymaga Pester/mock lub deterministycznego fixture testu.
