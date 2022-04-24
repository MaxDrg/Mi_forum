FROM python:3.6.9

WORKDIR /bot

COPY requirements.txt /bot

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .