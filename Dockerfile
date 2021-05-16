FROM mirror.sunwoda.com/apseasy/python:3.8.1

RUN apt update && \
	apt install -y \
		supervisor cron vim screen && \
		rm -rf /var/lib/apt/lists/*

COPY supervisor-app.conf /etc/supervisor/conf.d/
COPY . /code/
WORKDIR /code

RUN pip install -U pip --proxy=http://172.30.7.125:3128
RUN pip3 install -r requirements.txt  --proxy=http://172.30.7.125:3128

ENV REDIS_HOST="172.30.202.138" \
    PG_DATABASE="stockai" \
    PG_USER="stockai" \
    PG_PASSWORD="stockai" \
    PG_HOST="172.30.202.136" \
    PG_PORT="5432" \
    STATIC_FILE_URL="http://10.10.10.32:8000/" \
    Release="1"

EXPOSE 8000

CMD ["supervisord", "-n"]
