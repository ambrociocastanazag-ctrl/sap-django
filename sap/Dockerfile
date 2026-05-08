# Imagen base ligera y estable
FROM python:3.12-slim

# Variables que mejoran logs y reducen tamaño de imagen
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencias del sistema requeridas por psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python primero — mejora el cache de capas
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . .

EXPOSE 8000

# Comando por defecto (Compose lo sobreescribe en desarrollo)
CMD ["gunicorn", "sap.wsgi:application", "--bind", "0.0.0.0:8000"]