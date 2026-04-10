# Manual de operaciones

El presente manual tiene como propósito guiar en la configuración, despliegue y mantenimiento del proyecto __Lucy-Api__ en docker en entornos productivos.

## Índice

- [Manual de operaciones](#manual-de-operaciones)
  - [Índice](#índice)
  - [Requerimientos](#requerimientos)
  - [Inicio rápido](#inicio-rápido)
  - [Despliegue](#despliegue)
  - [Health check](#health-check)
  - [Automatizaciones](#automatizaciones)
  - [Mantenimiento](#mantenimiento)
    - [Monitoreo y Logs](#monitoreo-y-logs)
    - [Actualización de la Aplicación](#actualización-de-la-aplicación)
    - [Rollback Manual](#rollback-manual)

## Requerimientos

Es necesario disponer de docker instalado en el equipo host, adicionalmente también se recomienda tener descargadas las siguientes imágenes:

- Python 3.12-slim
- PostgreSQL 18 o superior
- Redis 8.6.2-alpine o superior

Por último es indispensable que las variables de entorno estén configuradas en su totalidad, con `PRODUCTION=True` y una secret de `DJANGO_SECRET_KEY` segura. Consulte las [variables de entorno](./virtual-env.md) para más información.

## Inicio rápido

A modo de ejemplo y despliegue pre-producción, se dispone de un [docker compose](../docker-compose.yml) pre-configurado para dicho fin. Esto para facilitar la detección de errores de producción en un entorno local controlado.

Ejecutar el compose

```sh
docker compose up -d
```

La distribución de puertos se encuentra repartida de la siguiente manera

- Backend -> 8000
- PostgreSQL -> ninguno
- Redis -> Ninguno

## Despliegue

Para desplegar la aplicación es necesario crear una imagen de la misma

```sh
docker build -t lucy_api .
```

Posteriormente crear un contenedor configurando todas las variables de entorno necesarias

```sh
# Linux / macOS
docker run -d --name lucy_api_app \
  -e 'PRODUCTION=True' \
  -e 'DJANGO_SECRET_KEY=your_secret_here' \
  ... \
  -p 8000:8000 lucy_api

# Windows
docker run -d --name lucy_api_app `
  -e 'PRODUCTION=True' `
  -e 'DJANGO_SECRET_KEY=your_secret_here' `
  ... `
  -p 8000:8000 lucy_api
```

## Health check

Una vez el contenedor se encuentre levantado y en ejecución, para comprobar que este esté disponible, debe de consultarse el endpoint `api/health/`, este debe de dar esta respuesta:

```json
{
  "status": "healthy"
}
```

## Automatizaciones

El proyecto utiliza GitHub Actions para automatizar el ciclo de vida de la aplicación. Estos flujos aseguran que el código sea de calidad y que el despliegue sea consistente.

| Workflow | Propósito |
| :--- | :--- |
| **Calidad (`quality.yml`)** | Ejecuta `pytest` y `ruff` para validar el código antes de la integración. |
| **Build (`build_image.yml`)** | Construye la imagen Docker y la sube al registro configurado. |
| **Deploy (`deploy.yml`)** | Despliega automáticamente la última versión construida en el entorno de producción. |
| **Deploy by Tag** | Permite desplegar una versión específica referenciada por un tag de Git. |
| **Rollback (`rollback.yml`)** | Facilita la reversión rápida a una versión estable anterior en caso de fallos. |

## Mantenimiento

Para garantizar la estabilidad del servicio en producción, se deben seguir estas pautas de mantenimiento.

### Monitoreo y Logs

Es fundamental revisar periódicamente los logs del contenedor para detectar anomalías:

```sh
docker logs -f lucy_api_app
```

### Actualización de la Aplicación

El proceso recomendado es a través del pipeline de CD. Sin embargo, si se requiere una actualización manual en el servidor:

1. Realizar un `pull` de la nueva imagen.
2. Detener y eliminar el contenedor actual.
3. Levantar el nuevo contenedor con las variables correspondientes (ver sección [Despliegue](#despliegue)).

### Rollback Manual

Si el workflow de `rollback.yml` falla o no se puede usar, se puede revertir manualmente ejecutando el contenedor con un tag de imagen anterior:

```sh
docker run -d --name lucy_api_app [PARAMETROS] lucy_api:vX.X.X
```

