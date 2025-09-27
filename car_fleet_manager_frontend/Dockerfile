# Frontend Dockerfile for Reflex
FROM python:3.11-slim

WORKDIR /frontend

COPY requirements.txt .
# Install system packages required by Reflex (bun installer needs unzip/curl)
RUN apt-get update \
    && apt-get install -y --no-install-recommends unzip curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install reflex \
    && which rx || true \
    && ls -l /root/.local/bin/rx || true

ENV PATH="/root/.local/bin:/usr/local/bin:$PATH"

COPY . .

EXPOSE 3000

CMD ["python", "-m", "reflex", "run", "--backend-host", "0.0.0.0", "--backend-port", "3000"]
