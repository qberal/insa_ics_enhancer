#! /usr/bin/env python3

import os
import regex
from icalendar import Calendar
import requests

# URL de votre fichier ICS
default_url = "https://cocktail.insa-rouen.fr/ics/edt-ade/2023-ITI3"
url = os.getenv("ICS_URL", default_url)

# Récupération du fichier ICS
response = requests.get(url)
cal = Calendar.from_ical(response.text)

groupes = []
# Parcourir les événements et les modifier selon les besoins
for component in cal.walk():
    desc = component.get('description')

    if desc is None:
        continue

    lines = desc.split('\n')

    for line in lines:
        if regex.match(r"[A-Z]+\d+(-\d+)?|[A-Z]+\d+", line):
            if line not in groupes:
                groupes.append(line)

    # Afficher les groupes trouvés pour cette description
print("Groupes trouvés:", groupes)