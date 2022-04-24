FROM python:3.7.13-bullseye

WORKDIR /bot

COPY requirements.txt /bot

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .