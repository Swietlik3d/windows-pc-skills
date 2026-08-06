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
