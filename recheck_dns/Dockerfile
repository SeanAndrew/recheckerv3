FROM python:3.8-buster

WORKDIR /usr/srv/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-u", "./app.py"]