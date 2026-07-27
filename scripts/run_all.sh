#!/bin/bash
set -e

echo "Starting CADFlow Stack..."
docker-compose up --build -d

echo "Stack is starting. Waiting for services to become healthy..."
sleep 10

echo "CADFlow is running!"
echo "Dashboard available at: http://localhost:8005"
echo "API Gateway available at: http://localhost:8000"
echo ""
echo "To test the pipeline, run:"
echo "bash scripts/test_webhook.sh"
