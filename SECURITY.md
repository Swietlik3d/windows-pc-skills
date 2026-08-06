# Bezpieczeństwo

Nie umieszczaj sekretów ani danych klienta w issue, commitach lub bundle. Podejrzany wyciek:
odłącz artefakt od przepływu, zachowaj minimalny dowód lokalnie, rotuj poświadczenie właściwym
kanałem i udokumentuj incydent bez wklejania sekretu. Nie przesyłaj go automatycznie.

Skrypty repair mają safety gates i nie są poleceniem wykonania. R3/R4 wymagają operatora, jawnego
targetu, backupu i rollbacku. Zgłoszenia podatności dotyczące repo należy przekazać prywatnym
kanałem właściciela; repo nie definiuje publicznego endpointu.
