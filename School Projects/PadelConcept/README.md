# Padel Concept

Padel Concept er et Django-baseret webapplikation dedikeret til at fremme og organisere padelturneringer. Applikationen tilbyder funktioner som turneringstilmelding, visning af turneringsdetaljer, grupper og tidsplaner, samt administration af turneringer for administratorer.

## Funktioner

- Visning af kommende og afsluttede turneringer
- Tilmelding til turneringer
- Visning af grupper og stillinger
- Administration af turneringer via admin-panel
- Automatisk tidsplanlægning af kampe

## Installation

Følg disse trin for at installere og køre projektet i dit lokale miljø.

### Forudsætninger

- Python 3.8 eller nyere
- Git
- Virtuel miljø (anbefales)

### Trin 1: Klon repository

```bash
git clone https://github.com/dit-username/padel_concept.git
cd padel_concept
```

### Trin 2: Opret og aktiver virtuelt miljø

```bash
python -m venv venv
source venv/bin/activate
```

### Trin 3: Installer afhængigheder

```bash
pip install -r requirements.txt
```

### Trin 4: Opret og migrer database

```bash
python manage.py migrate
```

### Trin 5: Opret superbruger

```bash
python manage.py createsuperuser
```

### Trin 6: Hent statiske filer

```bash
python manage.py collectstatic --noinput
```

### Trin 7: Kør server

```bash
python manage.py runserver
```

### Trin 8: Åbn browser
Gå til `localhost:8000` i din browser for at se applikationen.
Eller `localhost:8000/admin` for at logge ind i admin-panelet.