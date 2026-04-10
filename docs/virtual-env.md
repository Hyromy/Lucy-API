# Variables de entorno

El proyecto se ejecuta por defecto en modo desarrollo `PRODUCTION=False` con una configuración minima para funcionar.

Para configurar manualmente dichas variables, crea una copia del archivo `.env.example` y en la raíz del proyecto renombrala como `.env`. A continuación se detallan las variables disponibles y su propósito:

## Índice
- [Variables de entorno](#variables-de-entorno)
  - [Índice](#índice)
  - [Configuración general](#configuración-general)
    - [`PRODUCTION`](#production)
    - [`DJANGO_SECRET_KEY`](#django_secret_key)
    - [`HOSTS`](#hosts)
    - [`CORS_ALLOWED`](#cors_allowed)
    - [`CSRF_TRUSTED`](#csrf_trusted)
  - [PostgreSQL](#postgresql)
    - [`PG_DB`](#pg_db)
    - [`PG_USER`](#pg_user)
    - [`PG_PASS`](#pg_pass)
    - [`PG_HOST`](#pg_host)
    - [`PG_PORT`](#pg_port)
  - [Discord](#discord)
    - [`DISCORD_CLIENT_ID`](#discord_client_id)
    - [`DISCORD_CLIENT_SECRET`](#discord_client_secret)
    - [`DISCORD_REDIRECT_URI`](#discord_redirect_uri)


## Configuración general

### `PRODUCTION`
Define el modo de ejecución del proyecto entre desarrollo (`False`) y producción (`True`).

_Por defecto, toma el valor de `False`._

### `DJANGO_SECRET_KEY`
Secret de seguridad para protecciones y criptografía del proyecto. Se recomienda configurar un secret con caracteres combinados y de al menos 50 caracteres de longitud.

_Por defecto, se establece una secret insegura_.

### `HOSTS`
Hosts permitidos para ser el anfitrión del proyecto. Puede definirse más de uno separandolo por comas (`,`).

_Por defecto, en desarrollo se permiten todos los hosts_

> Ejemplo
> 
> HOSTS=site.example.com, other.site.com

### `CORS_ALLOWED`
Hosts externos (frontend) que pueden solicitar información al proyecto. Puede definirse más de uno separandolo por comas (`,`).

Generalmente se esperan tener los mismos valores que [CSRF_TRUSTED](#csrf_trusted).

_Por defecto, en desarrollo se permiten todos los hosts_

> Ejemplo
>
> CORS_ALLOWED=https://my.site.com, https://super_web.com

### `CSRF_TRUSTED`
Hosts externos (frontend) que pueden enviar información o formularios al proyecto. Puede definirse más de uno separandolo por comas (`,`).

Generalmente se espera tener los mismos valores que [CORS_ALLOWED](#cors_allowed)

> Ejemplo
>
> CSRF_TRUSTED=https://my.site.com, https://super_web.com

## PostgreSQL

> [!Warning]
> Todas las variables de esta sección son obligatorias si el proyecto se ejecuta en modo producción

### `PG_DB`
Nombre de la base de datos PostgreSQL a conectarse.

### `PG_USER`
Usuario de PostgreSQL a conectarse.

### `PG_PASS`
Contraseña del usuario de PostgreSQL a conectarse.

### `PG_HOST`
Host o anfitrión de la base de datos PostgreSQL.

Suele ser `localhost`, una IP o dominio.

### `PG_PORT`
Puerto de la base de datos PostgreSQL.

Suele el `5432`.

## Discord

> [!Warning]
> Todas las variables de esta sección son obligatorias si se hará uso de la [aplicación de autenticación](../apps/_auth/)

> [!Note]
> Puedes conseguir estas variables en el [Discord Developer Portal](https://discord.com/developers/applications)

### `DISCORD_CLIENT_ID`
Identificador de la aplicación del cliente de discord.

### `DISCORD_CLIENT_SECRET`
Secret de seguridad de autenticación para el id de cliente de discord.

### `DISCORD_REDIRECT_URI`
URL de redireccionamiento seguro cuando el usuario autorice la interacción con discord.

El proyecto solo permite configurar una, pero [Discord Developer Portal](https://discord.com/developers/applications) permite la configuración de multiples valores.

_Por defecto este tiene la terminación `auth/discord/callback/`_

> Ejemplo
>
> DISCORD_REDIRECT_URI=http://localhost:8000/auth/discord/callback/
> DISCORD_REDIRECT_URI=http://my.backend.com/auth/discord/callback/
