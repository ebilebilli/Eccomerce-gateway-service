#!/bin/bash
set -e

echo "Starting API Gateway..."
echo "PORT environment variable: ${PORT:-8080}"
echo "SHOP_SERVICE: ${SHOP_SERVICE:-http://localhost:8001}"
echo "SHOPCART_SERVICE: ${SHOPCART_SERVICE:-http://localhost:8002}"

# Check if gateway directory exists
if [ ! -d "/app/gateway" ]; then
    echo "ERROR: gateway directory not found!"
    ls -la /app/
    exit 1
fi

# Check if main.py exists
if [ ! -f "/app/gateway/main.py" ]; then
    echo "ERROR: gateway/main.py not found!"
    ls -la /app/gateway/
    exit 1
fi

echo "Starting uvicorn server..."
exec uvicorn gateway.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers
