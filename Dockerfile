FROM python:3.12-slim

WORKDIR /app

# Install system deps + Node.js 20
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build frontend
RUN cd frontend && npm install && npm run build

# Collect static (includes built frontend)
RUN python manage.py collectstatic --noinput

RUN chmod +x docker_start.sh

CMD ["./docker_start.sh"]
