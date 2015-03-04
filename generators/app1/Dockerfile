FROM orchardup/python:2.7
ENV PYTHONBUFFERED 1
RUN apt-get update -q
RUN apt-get install rsyslog
RUN mkdir /code
WORKDIR /code
ADD ./app/ /code/
