FROM python:3.9.5-slim-buster

RUN mkdir -p /opt/app
COPY requirements.txt /opt/app/requirements.txt
RUN pip install --upgrade pip

# ensure we can run the make commands
RUN apt-get update -y && \
 	apt-get install -y make && \
    apt-get install -y git && \
 	apt-get install -y libffi-dev gcc && \
 	# for swagger
 	apt-get install -y curl && \
    # for postgres driver
 	apt-get install -y libpq-dev


RUN pip install -r /opt/app/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/opt/app/"
COPY Makefile /opt/app/Makefile
COPY api /opt/app/api
COPY run.py /opt/app/run.py
WORKDIR /opt/app
