# ---------------------------------------------------------------
# Imagen para el Sistema de Gestion Universitaria (Django)
# ---------------------------------------------------------------
FROM python:3.10-slim

# Evita archivos .pyc y fuerza salida sin buffer (logs en tiempo real)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=universidad_project.settings

WORKDIR /app

# Dependencias del sistema necesarias para psycopg2 y para esperar a Postgres
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Se copia primero requirements.txt para aprovechar la cache de capas:
# si el codigo cambia pero las dependencias no, no se reinstala nada.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Ahora si, el codigo de la aplicacion
COPY . .

# El bit de ejecucion no sobrevive a Git en Windows: se fuerza aqui.
# staticfiles se crea ANTES del chown para que el volumen de Compose que se
# monta en esa ruta herede el propietario appuser y no root.
RUN chmod +x /app/entrypoint.sh && mkdir -p /app/staticfiles

# Usuario sin privilegios (buena practica de seguridad)
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "universidad_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
