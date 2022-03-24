FROM python:3.9-alpine

RUN mkdir -p /home/brevet/web

WORKDIR /home/brevet

# Setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1

# Install pre-reqs
RUN pip install --upgrade pip
# psycopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# pillow
RUN apk add zlib-dev jpeg-dev gcc musl-dev

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install application
COPY . /home/brevet/web

# Create user and set ownership
RUN addgroup -S  brevet 
RUN adduser -S brevet -G brevet
RUN chown -R brevet:brevet /home/brevet
USER brevet