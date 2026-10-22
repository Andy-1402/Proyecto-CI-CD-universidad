# Sistema de Gestión Universitaria — Proyecto CI/CD

Proyecto académico de Integración y Despliegue Continuo sobre una aplicación
Django con PostgreSQL, contenerizada con Docker y automatizada con GitHub Actions.

## Estructura del repositorio

```
universidad_project/
├── .github/workflows/ci.yml      # Sesiones 1 y 3: pipeline CI/CD
├── docs/flujo-cicd-django.md     # Sesión 4: documento técnico + conclusiones
├── gestion/                      # App Django (Estudiante, Curso, tests)
├── universidad_project/          # Configuración del proyecto
├── Dockerfile                    # Sesión 2: imagen de la aplicación
├── docker-compose.yml            # Sesión 2: web + db
├── entrypoint.sh                 # Espera a Postgres, migra, collectstatic
├── deploy-notes.md               # Sesión 3: comandos de despliegue
├── requirements.txt
└── .env.example
```

## Ejecución local con Docker (recomendado)

```bash
cp .env.example .env
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

Luego abrir http://localhost:8000/ y http://localhost:8000/health/

## Ejecución local sin Docker

Requiere un PostgreSQL corriendo en `localhost:5432`.

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Pruebas

```bash
python manage.py test -v 2
```

Dos pruebas en `gestion/tests.py`:
- `CursoTests.test_creacion_curso_y_cupos_disponibles`
- `EstudianteTests.test_estudiante_se_matricula_en_curso`
