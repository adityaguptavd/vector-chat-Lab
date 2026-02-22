# -------- Stage 1: Build Dependencies --------
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------- Stage 2: Final Runtime --------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create non-root user
RUN useradd -m appuser

# Copy installed Python packages
COPY --from=builder /usr/local /usr/local

COPY . .

RUN mkdir -p /app/logs
RUN useradd -m appuser
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
