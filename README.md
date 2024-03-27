# INSA ICS Enhancer

Tired of having a not-so-good-schedule across your native calendar app?

INSA ICS Enhancer is here for you!

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
      - URL_ICS='https://cocktail.insa-rouen.fr/ics/edt-ade/2023-ITI3'
      - DESIRED_GROUPS="ITI32-APS-TD-02,ITI32-TD-02,ITI-32-PROGAV-TD-01,ITI32-TP2-1,ITI32-ESPAGNOL-RN-TD-01,ITI32-ANG-PG-TD-04"
```
### Choosing the Groups to Display
You can run the find_groups.py script to find available groups (note that you need to change the URL in the script, or set URL_ICS as an environment variable).

### Service Configuration
- URL_ICS: URL of the ICS feed to process
- DESIRED_GROUPS: List of groups to display, separated by commas

## Usage
You can access the schedule at http://localhost:3476/calendar.ics and subscribe to it in your favorite calendar app.