FROM python:3.10-slim

WORKDIR /app

COPY app_api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_api/ ./app_api/

ENV PYTHONPATH=/app

CMD ["python", "-m", "app_api.main"]
