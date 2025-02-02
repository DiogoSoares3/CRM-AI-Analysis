FROM python:3.12.8-slim

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl \
    git-all \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /PROJECT

COPY ./ /PROJECT

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
