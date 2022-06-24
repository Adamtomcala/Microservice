# Microservice
## Inštalácia:
Používal som verziu Pythonu 3.9.1.  
Pred prvý spustením je potrebné si nainštalovať knižnice. Inštaloval som knižnice:
- Django
- djangorestframework
- requests  

Ďalej je potrebné vytvoriť migrácie a ich aplikovať:
- python manage.py makemigrations
- python manage.py migrate

V Django projekte som vytvoril 2 aplikácie: app a api. Dve aplikácie som vytvoril preto, lebo cez FE som nevedel správne poslať PUT a DELETE request, 
tak v aplikácií som to implementoval a testoval pomocou nástroja PostMan.  

### App
- V tejto aplikácií som sa pokúsil splniť zadanie aj s implementáciou FE. Vytvoril som v nej jeden model pre príspevky a k nemu jeho serializer.
- Zadanie som riešil tak, že ak používateľ chce vyhľadať príspevok na základe jeho ID, zobrazia sa informácie o danom príspevku.
- Ak používateľ chce hľadať príspevok podľa user ID, tak sa zobrazia všetky príspevky daného používateľa.
- Na úvodnej stránke som vytvoril formuláre, podľa ktorých sa hľadá príspevok.
- Na navigačnej lište sa nachádzajú linky stránky Create, Delete a Update príspevku.
- Pri vyvtváraní musí používateľ vyplniť všetky políčka a vytvorí sa príspevok.
- Pri vymazaní príspevku musí používateľ zadať jeho ID.
- Pri aktualizácií musí používateľ najskôr zadať ID príspevku, následne bude presmerovaný na stránku, kde sa mu zobrazí body a title príspevku a môže zmeniť title
alebo body.

### Api
- V tejto aplikácií som riešil zadanie tak, že vraciam iba Json objekty. Vytvoril som v nej takisto jeden model a serializer (rovnaký)
- Dobyty na jednotlivé endpointy som testoval pomocou nástroja PostMan.

- kontajnerizáciu som nesplnil.
- na zadaní som pracoval cca 15 hodín.
- priložil som aj API dokumentáciu vo fromáte .yaml.
