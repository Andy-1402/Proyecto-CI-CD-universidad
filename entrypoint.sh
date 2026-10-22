#!/bin/sh
set -e

# Espera a que PostgreSQL acepte conexiones antes de arrancar Django.
if [ -n "$POSTGRES_HOST" ]; then
  echo "Esperando a PostgreSQL en $POSTGRES_HOST:${POSTGRES_PORT:-5432} ..."
  until pg_isready -h "$POSTGRES_HOST" -p "${POSTGRES_PORT:-5432}" -U "$POSTGRES_USER" >/dev/null 2>&1; do
    sleep 1
  done
  echo "PostgreSQL disponible."
fi

# Migraciones y archivos estaticos en cada arranque del contenedor.
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
