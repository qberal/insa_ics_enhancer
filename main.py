#!/usr/bin/env python3

import os
from icalendar import Calendar
import requests

# URL de votre fichier ICS
default_url = "https://cocktail.insa-rouen.fr/ics/edt-ade/2023-ITI3"
url = os.getenv("URL_ICS", default_url)

# Récupération du fichier ICS
response = requests.get(url)
cal = Calendar.from_ical(response.text)

default_groups = "ITI32-APS-TD-02,ITI32-TD-02,ITI-32-PROGAV-TD-01,ITI32-TP2-1,ITI32-ESPAGNOL-RN-TD-01,ITI32-ANG-PG-TD-04"
groupesVoulus = os.getenv("GROUPES_VOULUS",default_groups).split(",")

for component in cal.walk():
    # supprimer les événements qui n'ont pas un des groupes voulus dans leur description
    desc = component.get('description')
    if desc is None:
        continue
    lines = desc.split('\n')

    aGroupeVoulu = False

    for line in lines:
        if line in groupesVoulus:
            aGroupeVoulu = True
            break

    if not aGroupeVoulu:
        if component['summary'] == "ITI32-PAO-PYTHON-TD-1":
            component['summary'] = "TD: PAO-PYTHON"
        else:
            cal.subcomponents.remove(component)
    else:
        # event c'est le titre de l'événement
        event = component.get('summary')
        parts = event.split("-")

        if parts[0] == "H":
            # Pour "H" : prendre le 3e (indice 2) et l'avant-dernier (indice -2) éléments (et inverser)
            selected_parts = f"{parts[-2]}: {parts[2]}"
        elif "PAO" in parts:
            # Pour "PAO" : traiter comme précédemment sans changement
            pao_index = parts.index("PAO")
            selected_parts = f"{parts[pao_index + 2]}: {' '.join(parts[pao_index:pao_index + 2])}"
        elif len(parts) > 2:
            # Pour les autres : prendre le 2e (indice 1) et le 3e (indice 2) éléments (et inverser)
            selected_parts = f"{parts[2]}: {parts[1]}"
        elif len(parts) == 2 and "examens" in lines:
            # Pour les autres : prendre le 2e (indice 1) et le 1er (indice 0) éléments (et inverser)
            selected_parts = f"Exam: {parts[1]}"
        else:
            # Pour les autres ne rien faire
            selected_parts = event
        # Remplacer le titre de l'événement par le nouveau titre
        component['summary'] = selected_parts

# Génération du nouveau fichier ICS
new_ical = cal.to_ical()
with open("calendrier.ics", "wb") as f:
    f.write(new_ical)
