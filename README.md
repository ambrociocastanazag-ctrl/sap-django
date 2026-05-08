# SAP — Sistema de Administración de Personas

Aplicación web Django para la gestión de personas y sus domicilios. Incluye autenticación con middleware custom, CRUD completo con búsqueda AJAX en tiempo real, panel de administración personalizado, paginación, settings divididos por entorno (dev/prod) con hardening de seguridad en producción, tests automatizados y deployment con Docker.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0.4-092E20?style=flat&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-passing-brightgreen?style=flat)

---

## Funcionalidades

- **Autenticación** — login y logout con `django.contrib.auth`, más un `LoginRequiredMiddleware` custom que protege todas las rutas excepto las explícitamente públicas
- **CRUD completo** — alta, edición, eliminación y listado de Personas y Domicilios con relación FK (Persona → Domicilio, `SET_NULL` on delete)
- **Búsqueda en tiempo real con AJAX** — filtrado dinámico sin recargar la página
- **Paginación** configurable vía `ITEMS_POR_PAGINA`
- **Panel de admin personalizado** con `verbose_names` y orden custom
- **Settings divididos** — `base / dev / prod` con flags de producción activos (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `ALLOWED_HOSTS` desde entorno)
- **Tests automatizados** con el test runner de Django
- **Docker-ready** — un solo `docker compose up` levanta API + base de datos

---

## Tech Stack

| Capa | Tecnología |
|------|-----------|
| Framework | Django 6.0.4 |
| Lenguaje | Python 3.12 |
| Base de datos | PostgreSQL 16 |
| Frontend | HTML5 + CSS3 + AJAX vanilla |
| Configuración | python-decouple |
| Deployment | Docker + docker-compose |

---

## Cómo correrlo

### Opción A — Docker (recomendado)

No requiere Python ni PostgreSQL instalados localmente.

```bash
git clone https://github.com/ambrociocastanazag-ctrl/sap-django.git
cd sap-django
docker compose up --build
```

App disponible en: http://localhost:8000
Postgres expuesto en el puerto **5433** del host (para evitar conflicto si ya tienes un Postgres local corriendo en 5432).

Para crear un superusuario:

```bash
docker compose exec web python manage.py createsuperuser
```

Panel de admin: http://localhost:8000/admin

### Opción B — Desarrollo local

**Requisitos:** Python 3.12+, PostgreSQL 14+

```bash
# 1. Clonar y crear entorno virtual
git clone https://github.com/ambrociocastanazag-ctrl/sap-django.git
cd sap-django
python -m venv .venv

# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de PostgreSQL

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Correr el servidor
python manage.py runserver
```

---

## Variables de entorno

Copia `.env.example` a `.env` y rellena:

```ini
SECRET_KEY=genera-una-clave-segura
DEBUG=True

DB_NAME=sap_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

Para generar un `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## Estructura del proyecto

```
sap-django/
├── sap/
│   ├── settings/
│   │   ├── base.py        # Configuración común
│   │   ├── dev.py         # Desarrollo (DEBUG=True)
│   │   └── prod.py        # Producción (SSL, ALLOWED_HOSTS, cookies seguras)
│   ├── urls.py
│   └── wsgi.py
├── webapp/
│   ├── middleware.py      # LoginRequiredMiddleware custom
│   ├── views.py
│   └── urls.py
├── personas/
│   ├── models.py          # Persona, Domicilio
│   ├── views.py           # CRUD + búsqueda AJAX
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
├── templates/
├── .env.example
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── requirements.txt
```

---

## Modelos

**Persona**
- `nombre` — CharField(255)
- `apellido` — CharField(255)
- `email` — EmailField, unique
- `domicilio` — FK a Domicilio, nullable, `SET_NULL` on delete, `related_name='personas'`

**Domicilio**
- `calle` — CharField(255)
- `no_calle` — CharField(20)
- `pais` — CharField(255)

Ambos modelos ordenan por `-id` (más recientes primero) y tienen `verbose_name` / `verbose_name_plural` configurados para el admin.

---

## Tests

```bash
# Local
python manage.py test

# Dentro de Docker
docker compose exec web python manage.py test
```

---

## Decisiones de diseño

**Settings divididos en tres archivos**
`base.py` contiene la configuración común. `dev.py` y `prod.py` heredan de base y sobreescriben solo lo necesario. `manage.py` apunta a `sap.settings.dev` por default; en producción se cambia con la variable de entorno `DJANGO_SETTINGS_MODULE=sap.settings.prod`.

**LoginRequiredMiddleware custom**
En lugar de decorar cada vista con `@login_required`, un middleware fuerza autenticación en toda la app excepto en las rutas públicas declaradas explícitamente. Menos código repetido, menos riesgo de olvidar proteger una vista.

**404 en cascada con `SET_NULL`**
Al borrar un Domicilio, las Personas asociadas no se eliminan — su campo `domicilio` queda en `NULL`. Evita pérdida accidental de datos de Personas por una operación sobre Domicilios.

---

## Author

**Gabriel Ambrocio** — Python Backend Developer
Guatemala City, Guatemala (UTC-6)

[GitHub](https://github.com/ambrociocastanazag-ctrl) · [LinkedIn](https://www.linkedin.com/in/gabriel-omar-ambrocio-castañaza-a72a1a2b3)
