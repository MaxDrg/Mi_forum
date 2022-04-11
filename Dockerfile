FROM python:3.8.10
# set work directory
WORKDIR /mi_forum
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
ENTRYPOINT ["/mi_forum/entrypoint.sh"]