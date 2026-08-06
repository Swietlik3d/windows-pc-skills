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
