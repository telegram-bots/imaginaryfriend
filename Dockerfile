FROM python:3.6.1-slim
ENV CONFIG_PATH "cfg/main.docker.cfg"
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
