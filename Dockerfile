FROM python:3.12-slim

WORKDIR /app

# System deps for psycopg + Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build React frontend so frontend/dist/ exists (enables WHITENOISE_ROOT)
RUN cd frontend && npm install && npm run build

# Collect Django static files
RUN python manage.py collectstatic --noinput

RUN chmod +x docker_start.sh

CMD ["./docker_start.sh"]
