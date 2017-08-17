FROM python:3.6.2-alpine3.6
ENV CONFIG_PATH "cfg/main.docker.cfg"
RUN mkdir /code/
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
CMD ["python", "-u", "run.py"]
