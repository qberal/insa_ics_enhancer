# Utilisez l'image officielle Python comme image de base
FROM python:3.12.2

RUN apt-get update && apt-get install -y cron lighttpd
RUN pip install icalendar requests

COPY main.py /root/script.py

RUN chmod +x /root/script.py
RUN echo "*/15 * * * * root python /root/script.py" > /etc/cron.d/cron_job
RUN echo "*/15 * * * * root cp calendrier.ics /var/www/html/calendrier.ics" > /etc/cron.d/cron_job
RUN chmod 0644 /etc/cron.d/cron_job
RUN touch /var/log/cron.log
RUN python /root/script.py
RUN cp /calendrier.ics /var/www/html/calendrier.ics

EXPOSE 80

CMD cron && lighttpd -D -f /etc/lighttpd/lighttpd.conf

