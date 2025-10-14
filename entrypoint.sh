#!/bin/bash
set -e

echo "Starting API Gateway..."
echo "PORT environment variable: ${PORT:-8080}"

exec uvicorn gateway.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers
