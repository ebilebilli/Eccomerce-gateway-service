# Use Python slim image
FROM python:3.13-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PORT=8080
ENV SHOP_SERVICE=http://localhost:8001
ENV SHOPCART_SERVICE=http://localhost:8002

# Set working directory
WORKDIR /app

# Copy pyproject.toml and lock file first
COPY pyproject.toml uv.lock ./

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install build \
    && pip install . --no-cache-dir

# Copy application code
COPY gateway/ ./gateway/

# Copy entrypoint script and make executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create non-root user and set ownership of /app
RUN useradd -m appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port for Cloud Run
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
