FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /login
COPY . /login/

RUN pip install -r requirements.txt

EXPOSE 8000
