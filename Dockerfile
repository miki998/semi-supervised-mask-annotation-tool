FROM pytorch/pytorch:latest
MAINTAINER Michael CHAN <miki998chan@gmail.com>

WORKDIR /home
COPY . .

RUN pip install -r requirements.txt && pip install jupyter
RUN apt-get update
RUN apt-get install vim

WORKDIR /home/DARK
RUN make
WORKDIR /home
EXPOSE 9999

STOPSIGNAL SIGTERM
