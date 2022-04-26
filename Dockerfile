FROM python:3.8.10
# set work directory
WORKDIR /m3_forum
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
    
# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
# copy project
COPY . .
# run entrypoint.sh
ENTRYPOINT ["/m3_forum/entrypoint.sh"]