FROM python:3.10.8-slim-bullseye

# Create work dir
RUN mkdir -p /restapi/
WORKDIR /restapi/

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
