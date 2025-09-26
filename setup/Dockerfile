FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Agora ele enxerga o requirements.txt da raiz
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia só a pasta setup para dentro do container
COPY setup /app/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
