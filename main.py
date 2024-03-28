#!/usr/bin/env python3
"""Main script to filter an ICS file based on the groups in the description."""
import os
import logging
import time

from icalendar import Calendar
import requests

if __name__ == "__main__":

    # Configuration du logger, avec niveau INFO, temps et message
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Starting script")

    # URL de l'ICS
    ICS_URL = os.getenv("ICS_URL", "https://cocktail.insa-rouen.fr/ics/edt-ade/2023-ITI3")
    GROUPS = os.getenv("GROUPS", "ITI3").split(",")
    EXTRA_CLASSES = os.getenv("EXTRA_COURSES", "").split(",")
    REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 5 * 60))

    REAL_NAME = {
        "APS": "Sport",
        "STAT": "Statistiques",
        "PROGAV": "Programmation avancée",
        "TSA": "Traitement de signaux aléatoires",
        "CAPT": "Capteurs",
        "DROIT": "Droit",
        "ANG": "Anglais",
        "TW1": "Technologies Web 1",
        "PYTHON": "Python",
        "ENT": "Entreprise et travail d'équipe",
        "CMR": "Conférences métiers et recherche",
        "COMPIL": "Compilation",
        "AUTO": "Automatique",
        "UMLDP": "UML et Design Patterns",
    }

    logging.info(f"URL: {ICS_URL}")
    logging.info(f"Selected groups: {GROUPS}")
    logging.info(f"Extra classes: {EXTRA_CLASSES}")

    while True:
        response = requests.get(ICS_URL)
        cal = Calendar.from_ical(response.text)

        for component in cal.walk():
            # supprimer les événements qui n'ont pas un des groupes voulus dans leur description
            desc = component.get('description')
            if desc is None:
                continue
            desc_lines = desc.split('\n')

            GROUPE_VOULU = any(line in GROUPS for line in desc_lines)

            if not GROUPE_VOULU and component['summary'] not in EXTRA_CLASSES:
                cal.subcomponents.remove(component)

            else:
                event_name = component.get('summary')
                event_name_splitted = event_name.split("-")

                if event_name_splitted[0] == "H":
                    new_event_name = f"{event_name_splitted[-2]}: {REAL_NAME.get(event_name_splitted[2], event_name_splitted[2])}"
                elif "PAO" in event_name_splitted:
                    pao_index = event_name_splitted.index("PAO")
                    new_event_name = f"PAO: {REAL_NAME.get(event_name_splitted[pao_index + 1], event_name_splitted[pao_index + 1])}"
                elif "examens" in desc_lines:
                    if "Machine" == event_name_splitted[-1]:
                        new_event_name = f"Exam: {REAL_NAME.get(event_name_splitted[1], event_name_splitted[1])} Machine"
                    else:
                        new_event_name = f"Exam: {REAL_NAME.get(event_name_splitted[1], event_name_splitted[1])}"
                elif len(event_name_splitted) > 2:
                    new_event_name = f"{event_name_splitted[2]}: {REAL_NAME.get(event_name_splitted[1], event_name_splitted[1])}"
                else:
                    logging.warning(f"{event_name} not matching any pattern, keeping as is.")
                    new_event_name = event_name

                component['summary'] = new_event_name

                desc_lines = component['description'].split('\n')
                desc_lines.pop(0)
                desc_lines.pop(0)
                desc_lines.pop(-2)
                component['description'] = "\n".join(desc_lines)


        # Génération du nouveau fichier ICS
        new_ical = cal.to_ical()
        with open("/var/www/html/calendrier.ics", "wb") as f:
            f.write(new_ical)

        logging.info("ics file generated successfully")
        time.sleep(REFRESH_INTERVAL)
