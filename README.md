# Git_Physical

# Dependencies:
  - python=3.11
  - numpy
  - pandas
  - random
  - matplotlib
  - matplotlib.backends.backend_tkagg
  - seaborn
  - itertools
  - time
  - datetime
  - tqdm
  - os
  - argparse
  - tkinter
  - PIL
  - ttkthemes

Instructies voor het verzamelen van resultaten met willekeurige borden:

1. Data genereren gaat met bijv. `python generate_data.py -r 1000 -s 9 -c 10 -cr 5`. 
Er kunnen verschillende parameters worden meegegeven, gebruik `python generate_data.py -h` voor een overzicht.

2. Data genereren kan even duren, afhankelijk van de gekozen parameters.
Na het genereren van de data wordt gevraagd of de onopgeloste borden ook opgeslagen moeten worden. 
Onopgeloste borden opslaan wordt alleen aangeraden bij een lage hoeveelheid runs.

De data wordt opgeslagen in 'data/experiment/'. De bestanden zijn als volgt genoemd
'size_startcars-endcars:date.csv' en eventueel 'unsolved_size_startcars-endcars:date.csv' voor de onopgeloste borden.

3. De resultaten kunnen worden gevisualiseerd met `python code_files/visualisation/data_analysis.py -s -n 25 -m 50`.
Gebruik `python code_files/visualisation/data_analysis.py -h` voor een overzicht van arguments.

4. Plots worden opgeslagen onder 'data/experiment_plots/' met argumenten in de naam.

Methodiek van het experiment dat je hiermee uitvoert:

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

