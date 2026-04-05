# Lucy API

Backend REST para el proyecto Lucy (Bot de Discord y Web)

![Django](https://img.shields.io/badge/Django-6.0.3-green?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.15.2-red?logo=django)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Poetry](https://img.shields.io/badge/Poetry-Package_Manager-blue?logo=poetry)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)

## Índice
- [Lucy API](#lucy-api)
  - [Índice](#índice)
  - [Variables de entorno](#variables-de-entorno)
  - [Instalación](#instalación)
    - [Poetry (Recomendado)](#poetry-recomendado)
    - [Pip](#pip)
    - [Docker](#docker)
  - [Ejecución](#ejecución)
    - [Desarrollo](#desarrollo)
    - [Producción (Docker)](#producción-docker)
  - [Despliegue y Mantenimiento](#despliegue-y-mantenimiento)
    - [Base de Datos](#base-de-datos)
    - [Superusuario](#superusuario)
  - [Diagnóstico y recuperación](#diagnóstico-y-recuperación)
    - [Logs](#logs)
    - [Arranque parcial](#arranque-parcial)
    - [Estado de la API](#estado-de-la-api)
    - [Sincronización de Base de Datos](#sincronización-de-base-de-datos)

## Variables de entorno

Para configurar el entorno, copia el archivo `.env.example` como `.env` en la raíz del proyecto.

```sh
cp .env.example .env
```

El proyecto detectará automáticamente si está en modo desarrollo o producción mediante la variable `PRODUCTION`.

## Instalación

### Poetry (Recomendado)

1. Instala las dependencias (el entorno virtual se gestiona solo):
   ```sh
   poetry install
   ```

2. (Opcional) Activa el entorno para ejecutar comandos directos de Django:
   ```sh
   poetry shell
   ```

### Pip

Si prefieres usar un entorno virtual tradicional con `pip`:

1. Crea y activa el entorno virtual:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

2. Instala Poetry (necesario para gestionar las dependencias del `pyproject.toml`):
   ```sh
   pip install poetry
   ```

3. Instala las dependencias:
   ```sh
   poetry install
   ```

### Docker

Construye la imagen optimizada para el VPS:
```sh
docker build -t lucy-api .
```

## Ejecución

### Desarrollo
Para iniciar el servidor de desarrollo de Django:
```sh
poetry run python manage.py runserver
```

### Producción (Docker)
El contenedor arrancará automáticamente con Gunicorn, ejecutará migraciones y recolectará estáticos:
```sh
docker run -p 8000:8000 --env-file .env lucy-api
```

## Despliegue y Mantenimiento

### Base de Datos
- **Local:** Utiliza SQLite (`db.sqlite3`) de forma automática.
- **Producción:** Configura las variables `PG_...` en el `.env` para conectar con PostgreSQL.

### Superusuario
Para crear un administrador en Docker, debes hacerlo manualmente una vez que el contenedor esté en ejecución:

1. Identifica el ID o nombre del contenedor:
   ```sh
   docker ps
   ```

2. Ejecuta el comando interactivo:
   ```sh
   docker exec -it <container_id> python manage.py createsuperuser
   ```

Sigue las instrucciones en la terminal para configurar el usuario, correo y contraseña.

## Diagnóstico y recuperación

### Logs
- En **Desarrollo**, los logs se muestran directamente en la terminal.
- En **Producción**, Django y Gunicorn están configurados para enviar logs a `stdout` (consola de Docker). Puedes consultarlos con:
  ```sh
  docker logs -f <container_id>
  ```

### Arranque parcial
Si el contenedor o el servidor no arranca, lo más común es una variable de entorno faltante. Revisa el archivo `.env` contrastándolo con `.env.example`.

### Estado de la API
Para verificar que la API está operativa, puedes acceder al endpoint de salud o al panel de administración: `http://localhost:8000/admin/`

### Sincronización de Base de Datos
Si tras un `git pull` el proyecto falla, asegúrate de ejecutar las migraciones:
```sh
poetry run python manage.py migrate
```
En Docker, esto se hace automáticamente al arrancar el contenedor.
