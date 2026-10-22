# Notas de Despliegue — Sistema de Gestión Universitaria

Guía de los comandos exactos para desplegar el proyecto en un servidor externo
(VPS Ubuntu 22.04, AWS EC2, DigitalOcean, Azure VM, etc.).

---

## 1. Conexión al servidor

```bash
ssh usuario@IP_DEL_SERVIDOR
```

## 2. Instalar Docker y Docker Compose (solo la primera vez)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl

# Instalación oficial de Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Permitir usar docker sin sudo
sudo usermod -aG docker $USER
newgrp docker

# Verificar
docker --version
docker compose version
```

## 3. Descargar el proyecto desde GitHub

```bash
cd /opt
sudo mkdir -p apps && sudo chown $USER:$USER apps
cd apps

git clone https://github.com/USUARIO/universidad_project.git
cd universidad_project
```

Si el repositorio ya existía en el servidor, basta con actualizarlo:

```bash
cd /opt/apps/universidad_project
git pull origin main
```

## 4. Configurar las variables de entorno

```bash
cp .env.example .env
nano .env
```

Contenido mínimo a ajustar en `.env`:

```bash
DJANGO_SECRET_KEY=una-clave-larga-y-aleatoria-generada-para-produccion
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=IP_DEL_SERVIDOR,midominio.com

POSTGRES_DB=universidad_db
POSTGRES_USER=universidad_user
POSTGRES_PASSWORD=una-password-fuerte
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Generar una SECRET_KEY segura:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

## 5. Levantar la aplicación con Docker Compose

```bash
# Construir las imágenes y levantar los contenedores en segundo plano
docker compose up -d --build

# Ver el estado de los servicios
docker compose ps

# Ver los logs en tiempo real
docker compose logs -f web
```

Salida esperada de `docker compose ps`:

```
NAME               IMAGE                       STATUS                   PORTS
universidad_db     postgres:15                 Up (healthy)             0.0.0.0:5432->5432/tcp
universidad_web    universidad_project-web     Up                       0.0.0.0:8000->8000/tcp
```

## 6. Tareas post-despliegue

```bash
# Las migraciones y collectstatic ya corren solas en el entrypoint,
# pero se pueden forzar manualmente:
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput

# Crear el usuario administrador
docker compose exec web python manage.py createsuperuser
```

## 7. Validación en el navegador

Abrir desde cualquier equipo:

| Recurso            | URL                                      | Resultado esperado                         |
|--------------------|------------------------------------------|--------------------------------------------|
| Endpoint principal | `http://IP_DEL_SERVIDOR:8000/`           | JSON con contadores de estudiantes y cursos |
| Health check       | `http://IP_DEL_SERVIDOR:8000/health/`    | `{"status": "ok"}`                          |
| Panel admin        | `http://IP_DEL_SERVIDOR:8000/admin/`     | Formulario de login de Django               |

Validación desde la terminal del servidor:

```bash
curl -i http://localhost:8000/health/
# Esperado: HTTP/1.1 200 OK  ->  {"status": "ok"}
```

Si el puerto está bloqueado, abrir el firewall:

```bash
sudo ufw allow 8000/tcp
sudo ufw reload
```

## 8. Comandos de mantenimiento

```bash
# Reiniciar solo la aplicación
docker compose restart web

# Detener todo (conserva los datos)
docker compose down

# Detener y BORRAR la base de datos (destructivo)
docker compose down -v

# Actualizar a la última versión del código
git pull origin main
docker compose up -d --build

# Backup de la base de datos
docker compose exec db pg_dump -U universidad_user universidad_db > backup_$(date +%F).sql

# Restaurar un backup
cat backup_2026-10-22.sql | docker compose exec -T db psql -U universidad_user universidad_db
```

## 9. Despliegue a partir de la imagen de DockerHub (flujo real)

Cuando el job `build-docker` publique la imagen en DockerHub, el servidor ya no
necesita compilar nada:

```bash
docker login
docker pull USUARIO_DOCKERHUB/universidad-web:latest
docker compose up -d
```

## 10. Solución de problemas frecuentes

| Síntoma                                     | Comando de diagnóstico                      | Causa habitual                               |
|---------------------------------------------|---------------------------------------------|----------------------------------------------|
| `web` reinicia en bucle                     | `docker compose logs web`                   | Falta `.env` o credenciales de BD incorrectas |
| `could not connect to server`               | `docker compose ps db`                      | El contenedor `db` aún no está *healthy*      |
| `DisallowedHost at /`                       | `grep ALLOWED .env`                         | Falta la IP/dominio en `DJANGO_ALLOWED_HOSTS` |
| La web no responde desde fuera              | `sudo ufw status`                           | Puerto 8000 cerrado en el firewall            |
