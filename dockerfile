FROM python:3.9-alpine

WORKDIR /home

# Setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1

# Install pre-reqs
# psycopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# pillow
RUN apk add zlib-dev jpeg-dev gcc musl-dev

# Install tools
RUN apk add nano

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --system

# Install application
COPY . /home

# Install cron jobs
COPY crontab .
RUN chmod 0644 crontab
RUN apk add supercronic shadow

# Create user and set ownership
RUN addgroup -S  brevet 
RUN adduser -S brevet -G brevet
RUN chown -R brevet:brevet /home
USER brevet