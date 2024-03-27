#!/usr/bin/env python3

import os
from icalendar import Calendar
import requests

# URL de votre fichier ICS
default_url = "https://cocktail.insa-rouen.fr/ics/edt-ade/2023-ITI3"
url = os.getenv("ICS_URL", default_url)

# Récupération du fichier ICS
response = requests.get(url)
cal = Calendar.from_ical(response.text)

default_groups = "ITI32-APS-TD-02,ITI32-TD-02,ITI-32-PROGAV-TD-01,ITI32-TP2-1,ITI32-ESPAGNOL-RN-TD-01,ITI32-ANG-PG-TD-04"
groupes_voulus = os.getenv("GROUPS", default_groups).split(",")

for component in cal.walk():
    # supprimer les événements qui n'ont pas un des groupes voulus dans leur description
    desc = component.get('description')
    if desc is None:
        continue
    lines = desc.split('\n')

    a_groupe_voulu = False

    for line in lines:
        if line in groupes_voulus:
            a_groupe_voulu = True
            break

    extra_classes = os.getenv("EXTRA_COURSES", "").split(",")

    if not a_groupe_voulu and component['summary'] not in extra_classes:
        cal.subcomponents.remove(component)
    else:
        event = component.get('summary')
        parts = event.split("-")

        if parts[0] == "H":
            selected_parts = f"{parts[-2]}: {parts[2]}"
        elif "PAO" in parts:
            pao_index = parts.index("PAO")
            selected_parts = f"{parts[pao_index + 2]}: {' '.join(parts[pao_index:pao_index + 2])}"
        elif len(parts) > 2:
            selected_parts = f"{parts[2]}: {parts[1]}"
        elif len(parts) == 2 and "examens" in lines:
            selected_parts = f"Exam: {parts[1]}"
        else:
            selected_parts = event

        component['summary'] = selected_parts

# Génération du nouveau fichier ICS
new_ical = cal.to_ical()
with open("calendrier.ics", "wb") as f:
    f.write(new_ical)
