# Instrukcje repozytorium

- Pisz dokumentację użytkową po polsku; polecenia, nazwy API i błędy zachowuj oryginalnie.
- Na hoście deweloperskim uruchamiaj wyłącznie walidatory, parsowanie fixture, mocki, pakowanie i
  operacje repo. Nigdy nie uruchamiaj repair `-Apply`, DISM/SFC, resetów, BCD, driverów ani firmware.
- Zbieraj dowody przed zmianą, klasyfikuj R0–R4, pokazuj target i rollback dla R2+.
- Nie zapisuj sekretów, PII, recovery keys ani danych klientów. `cases/` i dumpy pozostają poza Git.
- Fakty zależne od wersji wymagają source ID, `last_verified` i confidence. Community finding nie
  jest domyślną naprawą.
- Nie twierdź, że test przeszedł, jeżeli nie został wykonany. `SKIP` i `requires-live-validation`
  są prawidłowymi, uczciwymi wynikami.
- Używaj UTF-8/LF, kebab-case dla skilli, PascalCase-VerbNoun dla skryptów PowerShell.
- Zmiana procedury wymaga aktualizacji coverage matrix, playbook schema record, source register,
  tool manifest (jeśli dotyczy), evals i changelog.
- `_shared` nie może zawierać `SKILL.md`.
