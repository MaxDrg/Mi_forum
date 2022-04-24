FROM python:3.9.7-buster

WORKDIR /bot

COPY requirements.txt /bot

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .