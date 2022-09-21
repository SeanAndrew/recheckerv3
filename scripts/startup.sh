#!/bin/sh

echo "Starting startup.sh.."
echo "*/10       *       *       *       *       /usr/bin/python3 /usr/src/app/app.py" >> /etc/crontabs/root
crontab -l