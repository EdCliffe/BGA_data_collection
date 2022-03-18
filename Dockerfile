FROM python:3.8-slim-buster

RUN apt update -y
RUN apt install gnupg2 wget curl -y
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update && apt-get install -y google-chrome-stable
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN apt-get install -yqq unzip && \
 unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "./project/BGA_scraper.py" ]

