# Git_Physical

Voor dependencies, zie `environment.yml`.

Instructies voor het verzamelen van resultaten:

1. Data genereren gaat met `python generate_data.py`. 
Dit vraagt vervolgens user input voor een aantal parameters. De eerste drie hiervan zijn verplicht, de rest is optioneel.

2. Na de laatste parameter wordt de data gegenereerd. Dit kan even duren, afhankelijk van de gekozen parameters.
Na het genereren van de data wordt gevraagd of de onopgeloste borden ook opgeslagen moeten worden. 
Onopgeloste borden opslaan wordt alleen aangeraden bij een lage hoeveelheid runs.

De data wordt opgeslagen in 'data/experiment/'. De bestanden zijn als volgt genoemd
'size_startcars-endcars:date.csv' en eventueel 'unsolved_size_startcars-endcars:date.csv' voor de onopgeloste borden.


Methodiek van het experiment:

Er wordt een gridsearch uitgevoerd op de volgende parameters:
- size: de grootte van het bord
- numcars: het aantal auto's dat op het bord wordt geplaatst
- lock_limit: het minimale toegankelijke vakjes op een rij of kolom
- exit_distance: de minimale afstand tussen de rode auto en de uitgang

Met iedere combinatie van deze parameters wordt een boord gegenereerd en daar wordt ieder algoritme op uitgevoerd.

Dit gebeurt num_runs keer.

Het wordt aangeraden om maar 1 variable te laten variëren door er een range ervoor in te stellen.
Andere variaties kunnen beter in losse terminals worden uitgevoerd.

De resultaten worden later allemaal samengevoegd voor het maken van de plots.

