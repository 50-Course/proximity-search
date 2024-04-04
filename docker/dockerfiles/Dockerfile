FROM python:3.10-slim-buster

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY requirements.txt .

RUN poetry init --no-interaction
RUN cat requirements.txt | xargs  poetry add 

COPY . .

RUN echo "Success!"
