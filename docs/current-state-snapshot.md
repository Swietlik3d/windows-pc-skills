# Snapshot stanu — 2026-08-06

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
