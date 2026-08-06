# Bezpieczeństwo i autoryzacja

R0 wymaga prawa do odczytu urządzenia. R1 wymaga zgody na zmianę ustawienia użytkownika. R2 ma
backup i system-change approval. R3 wymaga pokazania dokładnego targetu oraz BitLocker readiness.
R4 wymaga wpisanego potwierdzenia targetu i zweryfikowanej kopii; agent nigdy nie wykonuje go
automatycznie.

Zakazane: password bypass, credential dumping, recovery-key extraction, BitLocker/EFS bypass,
piracka aktywacja, ukryta zdalna persistence, pracę wewnątrz PSU i flash przy niestabilnym
zasilaniu. Urządzenie domain/Entra/MDM pozostaje pod kontrolą organizacji.
