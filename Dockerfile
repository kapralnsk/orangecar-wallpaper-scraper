
FROM python:3.11-slim

# Use "RUN adduser -D -g '' newuser" for alpine
RUN adduser --disabled-password --gecos '' orangecar-scraper

WORKDIR /opt/orangecar-scraper

ENV VIRTUAL_ENV=/opt/orangecar-scraper/venv
RUN python3 -m venv $VIRTUAL_ENV && mkdir /tmp/imgstore
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install poetry
COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY src src/
COPY crontab.yaml crontab.yaml

USER orangecar-scraper

ENTRYPOINT ["yacron", "-c", "crontab.yaml"]