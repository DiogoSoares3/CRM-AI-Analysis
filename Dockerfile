FROM python:3.12.8-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /PROJECT

COPY ./ /PROJECT

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# CMD ["tail", "-f", "/dev/null"]