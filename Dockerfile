# =====================================================
# 🏗️ STAGE 1 — Build base image
# =====================================================
FROM python:3.11-slim AS builder

# Evitar archivos .pyc y logs bufferizados
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 y compilaciones
RUN apt-get update && apt-get install -y \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias en un directorio aislado
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# =====================================================
# 🧱 STAGE 2 — Final image
# =====================================================
FROM python:3.11-slim

# Crear usuario no root
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# Copiar dependencias desde el builder
COPY --from=builder /install /usr/local

# Copiar el resto del código del servicio
COPY . .

# Variables de entorno
ENV ENVIRONMENT=production
ENV PYTHONPATH=/app

# Puerto expuesto (por defecto FastAPI)
EXPOSE 8000

# Cambiar a usuario seguro
USER appuser

# Comando de ejecución (Uvicorn + FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
