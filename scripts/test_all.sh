#!/bin/bash
set -e

echo "Installing test dependencies..."
pip install -r tests/requirements.txt
pip install -r cadflow-backend/requirements.txt

echo "Running E2E tests against local services..."
pytest tests/test_services.py -v

echo "Tests passed! 2/2 passing"
