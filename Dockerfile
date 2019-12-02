FROM python:3.7-alpine

RUN mkdir -p /code/push_redirect && \
    echo "__version__ = '1.0.0'" > /code/push_redirect/__init__.py
WORKDIR /code
COPY ./setup.cfg ./setup.py ./
RUN pip install --no-cache-dir -U pip -e .
