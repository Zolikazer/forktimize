#!/bin/sh
set -e

echo "📦 Running migrations..."
python migration.py

echo "🚀 Starting FastAPI app..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
