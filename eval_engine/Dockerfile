FROM python:3.11-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY eval_service.py ./

EXPOSE 8000

CMD ["uvicorn", "eval_service:app", "--host", "0.0.0.0", "--port", "8000"]
