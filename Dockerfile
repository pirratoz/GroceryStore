FROM python:3.10.8-slim-bullseye

# Create work dir
RUN mkdir -p /restapi/
WORKDIR /restapi/
RUN mkdir -p /grocery/certs

# Certs generate
RUN openssl genrsa -out /grocery/certs/jwt-private.pem 2048
RUN openssl rsa -in /grocery/certs/jwt-private.pem -outform PEM -pubout -out /grocery/certs/jwt-public.pem

# Cache
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy source
COPY imageworker imageworker
COPY grocery grocery
COPY alembic alembic
COPY alembic.ini .
COPY main.py .
