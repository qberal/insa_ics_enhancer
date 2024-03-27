# INSA ICS Enhancer

Tired of having a not-so-good-schedule across your native calendar app?

INSA ICS Enhancer is here for you!

This service allows you to filter the groups you want to display in your calendar, and subscribe to it in your favorite calendar app. It's a simple python script and a small web server that will update every 15 minutes.

## Setup

Use Docker Compose to host the service on your server. You can configure the groups to display in the environment variables.

You can also use the dockerfile to build the image and run it manually.

### Docker Compose Configuration

```yml
services:
  insa_ics:
    image: ghcr.io/qberal/insa_ics:latest
    ports:
      - "3476:80"
    environment:
      - TZ=Europe/Paris
      - ICS_URL=https://cocktail.insa-rouen.fr/ics/edt-ade/2023-ITI3
      - GROUPS=ITI32-APS-TD-02,ITI32-TD-02,ITI-32-PROGAV-TD-01,ITI32-TP2-1,ITI32-ESPAGNOL-RN-TD-01,ITI32-ANG-PG-TD-04
      - EXTRA_COURSES=ITI32-PAO-PYTHON-TD-1,H-32-SME-CHORALE-ECAO-TD-1
      - REFRESH_INTERVAL=300
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80"]
```

### Service Configuration
- `TZ`: Timezone of the calendar (for logs)
- `ICS_URL`: URL of the ICS feed to process
- `GROUPS`: List of groups to display. separated by commas
- `EXTRA_COURSES`: List of names of courses to display, when not in specific groups. separated by commas
- `REFRESH_INTERVAL`: Interval in seconds between each refresh of the ICS feed (in seconds)

### Choosing the Groups to Display
You can run the find_groups.py script to find available groups (note that you need to change the URL in the script, or set `URL_ICS` as an environment variable).

#### Available ITI3 Groups:

- ITI31-TP-GR-04
- ITI31-TP-GR-03
- ITI32-ALLEMAND-TD-01
- ITI31-TP-GR-01
- ITI31-TP-GR-02
- ITI32-TD-02
- ITI32-TD-01
- ITI32-APS-TD-01
- ITI31-ALLEMAND-TD-01
- ITI32-ESPAGNOL-RN-TD-01
- ITI32-TP2-1
- ITI32-TP2-2
- ITI32-TP1-2
- ITI32-TP1-1
- ITI31-ESPAGNOL-RN-TD-01
- ITI32-ANG-PG-TD-04
- ITI32-ANG-PG-TD-03
- ITI32-FLE-TD-01
- CGC32-FLE-TD-01
- ITI31-ANG-PG-TD-02
- ITI32-ALLEMAND-TD-02
- ITI31-ALLEMAND-TD-02
- ITI32-ANG-PG-TD-02
- ITI32-ANG-PG-TD-01
- ITI32-APS-TD-03
- ITI32-APS-TD-02
- ITI31-APS-TD-02
- ITI31-ANG-PG-TD-04
- ITI31-ANG-PG-TD-03
- ITI31-FLE-TD-01
- ITI31-ANG-PG-TD-01
- ITI31-APS-TD-01
- ITI31-ESPAGNOL-TD-01
- ITI32-ESPAGNOL-TD-01


## Usage
You can access the schedule at http://localhost:3476/calendrier.ics and subscribe to it in your favorite calendar app.
