FROM python:3.12-slim AS prod

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_MODE prod

COPY ./requirements.txt /requirements.txt

RUN pip3 install --no-cache-dir -r /requirements.txt

ENV PYTHONPATH /project/source:/libs

WORKDIR /project/source