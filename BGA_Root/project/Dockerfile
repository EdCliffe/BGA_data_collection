FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt 

COPY . .

CMD [ "python", "./Project/BGA_scraper.py" ]
