FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# We can run both uvicorn and celery from here by overriding the command in docker-compose.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
