# Download framework

Jedynym entrypointem jest `scripts/toolkit/Get-VerifiedServiceTool.ps1`. Downloader rozwiązuje
exact version, pokazuje licencję/rozmiar, wymaga `-AcceptLicense`, pobiera do temp, weryfikuje
hash/signature, zapisuje provenance i nigdy nie uruchamia assetu. W repo nie ma assetów.
