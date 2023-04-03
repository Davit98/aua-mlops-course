FROM python:3.9-alpine
WORKDIR /application

COPY ./requirements.txt requirements.txt
RUN apk add --no-cache \
		gcc \
		libc-dev \
		linux-headers \
		bash; \
	pip install -r requirements.txt;

COPY . .

EXPOSE 5000
VOLUME /application

# gunicorn (uWSGI) is a wsgi server which we need for Flask to work with prometheus client
CMD gunicorn --workers=1 --bind 0.0.0.0:5000 application:application

