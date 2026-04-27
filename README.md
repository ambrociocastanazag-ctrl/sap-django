# SAP — Sistema de Administración de Personas

Aplicación web desarrollada con Django para la gestión de personas y domicilios.

## Tecnologías
- Python 3.12
- Django 6.0.4
- PostgreSQL
- HTML5 / CSS3

## Funcionalidades
- Autenticación con login y logout
- CRUD completo de personas y domicilios
- Búsqueda en tiempo real con AJAX
- Paginación
- Panel de administración personalizado
- Tests automatizados

## Instalación

1. Clona el repositorio
   git clone https://github.com/ambrociocastanazag-ctrl/sap-django.git

2. Crea y activa el entorno virtual
   python -m venv .venv
   .venv\Scripts\activate

3. Instala las dependencias
   pip install -r requirements.txt

4. Crea tu archivo .env basado en .env.example y rellena tus datos

5. Aplica las migraciones
   python manage.py migrate

6. Crea un superusuario
   python manage.py createsuperuser

7. Corre el servidor
   python manage.py runserver


## Configuración de la base de datos

Este proyecto usa PostgreSQL. Antes de correr el proyecto:

1. Instala PostgreSQL desde https://www.postgresql.org/download/
2. Crea una base de datos
   - Abre pgAdmin o psql
   - Crea una base de datos llamada `sap_db` (o el nombre que prefieras)
3. Configura tu `.env` con los datos de tu base de datos
   DB_NAME=sap_db
   DB_USER=postgres
   DB_PASSWORD=tu_password
   DB_HOST=localhost
   DB_PORT=5432
