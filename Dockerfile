FROM python:3.6.2-alpine3.6
ENV CONFIG_PATH "cfg/main.docker.cfg"
ENV LIBRARY_PATH=/lib:/usr/lib
RUN mkdir /code/
WORKDIR /code
ADD requirements.txt /code/
RUN apk add --no-cache build-base jpeg-dev zlib-dev && pip install -r requirements.txt && apk del build-base
ADD . /code/
CMD ["python", "-u", "run.py"]
