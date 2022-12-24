FROM bitnami/python:3.11-debian-11
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt
RUN mkdir /worker
WORKDIR /worker