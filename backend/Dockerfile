FROM python:alpine
WORKDIR /code/server
RUN apk update && apk add --update --no-cache --virtual .tmp musl-dev linux-headers openssl-dev g++ libffi-dev python3-dev build-base
COPY . .
RUN pip install -U setuptools
RUN pip install -r requirements.dev.txt
RUN pip install supervisor
RUN apk del .tmp
EXPOSE 5000
CMD ["supervisord", "-c", "services-script.conf"]