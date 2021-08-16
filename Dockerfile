  
FROM python:3.9-slim

# Use "RUN adduser -D -g '' newuser" for alpine
RUN adduser --disabled-password --gecos '' orangecar-scraper

WORKDIR /opt/orangecar-scraper

ENV VIRTUAL_ENV=/opt/orangecar-scraper/venv
RUN python3 -m venv $VIRTUAL_ENV && mkdir /tmp/imgstore
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install \
    --trusted-host pypi.org \
    --disable-pip-version-check \
    -r requirements.txt

COPY src src/
COPY crontab.yaml crontab.yaml

USER orangecar-scraper

ENTRYPOINT ["yacron", "-c", "crontab.yaml"]