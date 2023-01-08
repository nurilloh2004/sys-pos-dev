FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /code

COPY . /code/
RUN pip install -r /code/requirements/dev.txt

WORKDIR /code
