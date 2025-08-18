# Frontend Dockerfile for Reflex
FROM python:3.11-slim

WORKDIR /frontend

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install reflex \
    && which rx || true \
    && ls -l /root/.local/bin/rx || true

ENV PATH="/root/.local/bin:/usr/local/bin:$PATH"

COPY . .

EXPOSE 3000

CMD ["python", "-m", "reflex", "run", "--host", "0.0.0.0", "--port", "3000"]
