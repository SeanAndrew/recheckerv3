FROM python:3.8-alpine

WORKDIR /usr/srv/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD crontab /etc/cron.d/simple-cron
RUN chmod 0644 /etc/cron.d/simple-cron
RUN crontab /etc/cron.d/simple-cron

RUN touch /var/log/cron.log

COPY . .

CMD crond -l 2 && python -u ./app.py &&  tail -f /var/log/cron.log