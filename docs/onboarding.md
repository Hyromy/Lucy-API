# Manual de desarrollador

Lucy-API es una API REST diseñada para gestionar las funcionalidades del ecosistema Lucy. Este manual proporciona la información necesaria para configurar, desarrollar y desplegar el proyecto en entornos de desarrollo locales y seguros.

A modo de guía de inicio rápido, se recomienda consultar las secciones de [requerimientos](#requerimientos), [instalación](#instalación) y [ejecución](#preparación-y-ejecución).

## Índice

- [Manual de desarrollador](#manual-de-desarrollador)
  - [Índice](#índice)
  - [Requerimientos](#requerimientos)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Variables de entorno](#variables-de-entorno)
  - [Instalación](#instalación)
    - [Dependencias](#dependencias)
      - [Poetry (recomendado)](#poetry-recomendado)
      - [Pip](#pip)
    - [Pre-commit](#pre-commit)
  - [Preparación y ejecución](#preparación-y-ejecución)
  - [Tests y revisiones](#tests-y-revisiones)
  - [Mantenimiento y correcciones](#mantenimiento-y-correcciones)
    - [Migraciones y DB](#migraciones-y-db)
    - [Gestión de la DB](#gestión-de-la-db)
    - [Mantenimiento de tests](#mantenimiento-de-tests)
  - [Flujo colaborativo](#flujo-colaborativo)
    - [Ramas](#ramas)
    - [Pull requests](#pull-requests)
    - [Workflows](#workflows)

## Requerimientos

Se necesita una instalación de __Python 3.12__ para ejecutar el proyecto, además de las [dependencias](../pyproject.toml), también se necesitan herramientas adicionales:

- Poetry
- PostgreSQL
- Redis

> [!Warning]
> No se garantiza compatibilidad con versiones previas o posteriores de Python 3.12

## Estructura del proyecto

El proyecto dispone de la estructura estándar de Django, a continuación se detallan solo las carpetas y archivos relevantes.

- `apps/`: Núcleo lógico del proyecto.
  - `_auth/`: Mecanismos de autenticación mediante OAuth2.
  - `api/`: Modelos y serializadores de la API RESTFUL.
- `docs/`: Documentación detallada del proyecto.
- `project/`: Configuraciones generales del proyecto.
  - `config.py`: Configuraciones de variables de entorno.
  - `settings.py`: Configuraciones de comportamiento.
- `.env.example`: Plantilla de variables de entorno.
- `pyproject.toml`: Dependencias del proyecto.

A medida que se ejecuta y manipula el proyecto es posible que aparezcan archivos y carpetas como `db.sqlite3` o de cache.

> [!Tip]
> Si lo necesitas puedes generar archivos `.md` que incluyan la palabra _notes_, para realizar notas, apuntes, etc.

## Variables de entorno

Es posible ejecutar el proyecto sin configurar las variables de entorno, sin embargo las funciones de autenticación no estarán disponibles.

Consulte la configuración de [variables de entorno](./virtual-env.md) para más información.

## Instalación

El proyecto usa [poetry](https://python-poetry.org) como gestor de paquetes, en caso de no contar con el, también es posible instalar las dependencias mediante pip.

A fin de evitar duplicar las dependencias, se omite el archivo `requirements.txt`. Es necesario que la instalación mediante pip, instale la dependencia de poetry para interpretar correctamente las [dependencias](../pyproject.toml).

### Dependencias

#### Poetry (recomendado)

1. Instalación de dependencias
   ```sh
   poetry install
   ```

2. Activación del poetry shell
   ```sh
   poetry shell
   ```

#### Pip

1. Creación de entorno virtual
   ```sh
   python -m venv env
   ```

2. Activación de entorno virtual
   ```sh
   env\Scripts\activate       # Windows
   source env/bin/activate    # Linux / macOS
   ```

3. Instalación de poetry
   ```sh
   pip install poetry
   ```

4. Instalación de dependencias
   ```sh
   poetry install
   ```

### Pre-commit

Se utiliza para automatizar la revisión de formato y calidad de código antes de cada commit, asegurando que el historial de Git se mantenga limpio.

1. **Instalación de los hooks:**
   ```sh
   pre-commit install
   ```

A partir de este momento, cada vez que ejecutes `git commit`, se validarán automáticamente:
- Espacios en blanco innecesarios.
- Finales de archivo correctos.
- Formato y errores de Python mediante **Ruff**.

Si el pre-commit encuentra errores, detendrá el commit para que los revises (o los corregirá automáticamente si es posible).

Si necesitas ejecutarlo manualmente sobre todos los archivos sin hacer un commit:
```sh
pre-commit run --all-files
```

## Preparación y ejecución

Con las variables de entorno configuradas y las dependencias instaladas, es posible preparar y ejecutar el proyecto.

Ejecuta las migraciones
```sh
python manage.py migrate
```

> [!Note]
> En caso de que el proyecto este configurado en desarrollo `PRODUCTION=False` se crea o actualiza el archivo `db.sqlite3`.
>
> En caso contrario, se aplican las migraciones a la base de datos PostgreSQL configurada en las [variables de entorno](./virtual-env.md).

---

Ejecuta el proyecto

```sh
python manage.py runserver
```

## Tests y revisiones

A fin de garantizar la calidad del proyecto y evitar insertar errores sobre la funcionalidad del mismo, se recomienda ejecutar los tests y análisis estáticos.

Ejecuta los test

```sh
pytest
```

Ejecuta las revisiones de código y formato

```sh
ruff check
```

## Mantenimiento y correcciones

A medida que se desarrolla el proyecto es necesario realizar ciertas operaciones en el mismo para que este pueda adaptarse correctamente a los cambios del proyecto.

### Migraciones y DB

Para generar nuevas migraciones tras cambios en los modelos, crea y aplica las migraciones correspondientes.

```sh
python manage.py makemigrations    # Crea nuevas migraciones
python manage.py migrate           # Aplica las migraciones
```

### Gestión de la DB

Puede resultar útil manipular la información en la base de datos, para interactuar con ella desde el proyecto es necesario crear un usuario administrador

```sh
python manage.py createsuperuser
```

Seguir las instrucciones para crear el usuario, al finalizar ejecutar el proyecto y visitar la ruta `admin/`.

> [!Warning]
> Para crear el usuario administrador, las migraciones deben de estar aplicadas

### Mantenimiento de tests

Los tests definidos, no son infalibles. La finalidad de estos es garantizar la calidad del código y evitar romper funcionalidad existente a futuro.

Es posible que los requerimientos cambien, que se extienda o altere una o varias funcionalidades del proyecto, así como la detección de nuevos casos de borde. En cualquiera de esos casos es posible que los test fallen o que ya no tengan el alcance necesario, de ser así, se deben de actualizar los tests afectados.

## Flujo colaborativo

En caso de colaborar en el proyecto, y a fin de permitir un desarrollo consistente y flexible, se recomienda encarecidamente leer y respetar las secciones que se detallan a continuación.

### Ramas

Existen 2 ramas principales en el proyecto.

- `main`: Rama destinada a producción, cuenta con revisiones, tests, builds y despliegues automáticos.
- `dev`: Equivalente a __main__, sin integración a entornos productivos. Cuenta unicamente con revisiones y tests automáticos.

Otras ramas que vayan a ser creadas son de formato libre, independientemente de su propósito o longevidad.

### Pull requests

El formato de las pull request es abierto, siempre y cuando sea coherente, concreto y detallado (criterios subjetivos). Hay algunas restricciones que deben de seguirse para que estas se terminen integrando al proyecto.

1. Las ramas deben comenzar en `dev` u otras sub-ramas.
2. La pull request debe de pasar todas las revisiones y tests para ser considerada a integración.
3. Si agregas funcionalidad adicional, debes definir los tests correspondientes. Estos deben de ser realistas, y con una cobertura de los casos de borde como mínimo.
4. En caso de alterar los tests existentes, justificar el motivo en el cuerpo de la pull request.

En caso contrario la pull request puede ser rechazada o detenerse indefinidamente hasta que todos los puntos anteriormente mencionados queden resueltos. También es posible crear PR's de una sub-rama a otra.

En caso de que la pull request sea aceptada, esta debe de ser eliminada del repositorio remoto.

La rama __main__ únicamente recibe pull request de la rama __dev__.

### Workflows

Se disponen de varios workflows de GitHub Actions configurados, muchos de ellos destinados al CI y CD del proyecto, a continuación se detallan los workflows configurados y sus desencadenantes.

| Flujo | Descripción | Trigger |
| - | - | - |
| quality.yml | Ejecuta test y revisiones de código | PR's a __main__ o __dev__ |
| build_image.yml | Construye y publica imagen de docker del proyecto | Push a __main__ / Manual |
| deploy.yml | Despliega la versión más reciente en el VPS | Éxito en build / Manual |
| deploy-by-tag.yml | Despliegue de una versión específica (tag) | Reutilizable |
| rollback.yml | Revierte la versión a un tag específico | Manual |
