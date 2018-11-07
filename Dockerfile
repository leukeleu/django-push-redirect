FROM python:3.7

RUN mkdir /django
WORKDIR /django
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
