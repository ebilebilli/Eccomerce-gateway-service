#!/usr/bin/env sh
set -e

echo "Starting API Gateway..."

exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers
