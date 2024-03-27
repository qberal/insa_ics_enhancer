#!/usr/bin/env python3
"""Main script to filter an ICS file based on the groups in the description."""
import os
import logging
from icalendar import Calendar
import requests

# Configuration du logger, avec niveau INFO, temps et message
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Starting script")

# URL de l'ICS
DEFAULT_URL = "https://cocktail.insa-rouen.fr/ics/edt-ade/2023-ITI3"
URL = os.getenv("ICS_URL", DEFAULT_URL)

# Récupération du fichier ICS
response = requests.get(URL)
cal = Calendar.from_ical(response.text)

# Configuration des groupes, classes à garder
DEFAULT_GROUPS = ("ITI32-APS-TD-02,ITI32-TD-02,ITI-32-PROGAV-TD-01,ITI32-TP2-1,"
                  "ITI32-ESPAGNOL-RN-TD-01,ITI32-ANG-PG-TD-04")
groupes_voulus = os.getenv("GROUPS", DEFAULT_GROUPS).split(",")

extra_classes = os.getenv("EXTRA_COURSES", "").split(",")

logging.info(f"URL: {URL}")
logging.info(f"Selected groups: {groupes_voulus}")
logging.info(f"Extra classes: {extra_classes}")

for component in cal.walk():
    # supprimer les événements qui n'ont pas un des groupes voulus dans leur description
    desc = component.get('description')
    if desc is None:
        continue
    lines = desc.split('\n')

    A_GROUPE_VOULU = any(line in groupes_voulus for line in lines)

    if not A_GROUPE_VOULU and component['summary'] not in extra_classes:
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
            logging.warning(f"{event} not matching any pattern, keeping as is.")
            selected_parts = event

        component['summary'] = selected_parts


# Génération du nouveau fichier ICS
new_ical = cal.to_ical()
with open("calendrier.ics", "wb") as f:
    f.write(new_ical)

logging.info("ics file generated successfully")
