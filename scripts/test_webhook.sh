#!/bin/bash

# Simulates a GitHub Webhook payload for a PR
curl -X POST http://localhost:8000/webhook/github \
     -H "Content-Type: application/json" \
     -H "X-GitHub-Event: pull_request" \
     -d '{
       "action": "opened",
       "number": 42,
       "pull_request": {
         "head": {
           "sha": "abcdef1234567890"
         }
       },
       "filename": "sample.dxf"
     }'

echo ""
echo "Webhook sent! Check docker-compose logs for Celery worker output."
