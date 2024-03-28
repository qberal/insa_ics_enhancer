FROM python:3.12.2-slim

ENV ICS_URL=https://cocktail.insa-rouen.fr/ics/edt-ade/2023-ITI3
ENV GROUPS=ITI3
ENV REFRESH_INTERVAL=300

RUN apt-get update && apt-get install -y lighttpd curl
RUN pip install icalendar requests

COPY main.py /root/script.py

RUN chmod +x /root/script.py

CMD python /root/script.py & lighttpd -D -f /etc/lighttpd/lighttpd.conf
