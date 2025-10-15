FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8080

RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*

# copy project files first (so pip install sees the source)
COPY pyproject.toml .
COPY gateway/ ./gateway/

# install deps (editable ok if pyproject is configured)
RUN pip install --no-cache-dir -e .

# create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

# Use exec form and explicit port 8080 (Cloud Run expects this)
CMD ["uvicorn", "gateway.main:app", "--host", "0.0.0.0", "--port", "8080"]
