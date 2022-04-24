FROM python:3.7.0

WORKDIR /bot

COPY requirements.txt /bot

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .