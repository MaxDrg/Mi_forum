FROM python:3.7.0

WORKDIR /bot

COPY requirements.txt /bot

RUN pip3 install --upgrade pip3
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .