FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD sh -c 'set -e && \
    echo "Starting migrations..." && \
    python manage.py migrate --noinput --skip-checks 2>&1 && \
    echo "Migrations done. Starting gunicorn..." && \
    exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120 oromolegacy.wsgi:application'
