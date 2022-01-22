FROM python:3.9-slim-buster

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends apt-utils; \
    pip install -r requirements.txt; \
    rm -f requirements.txt; \
    apt-get clean; \
    apt-get autoclean; \
    apt-get purge -y; \
    rm -rf /root/.local/* /root/.cache/*; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*;

COPY *.py .

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app" ]
