# Problemas comunes

El presente documento recopila los problemas más frecuentes encontrados durante la instalación, despliegue y ejecución del proyecto __Lucy-API__, así como sus respectivas soluciones.

## Índice
- [Problemas comunes](#problemas-comunes)
  - [Índice](#índice)
  - [Base de Datos](#base-de-datos)
    - [Error al conectar con PostgreSQL](#error-al-conectar-con-postgresql)
    - [Migraciones pendientes](#migraciones-pendientes)
  - [Autenticación (Discord)](#autenticación-discord)
    - [Error `invalid_redirect_uri`](#error-invalid_redirect_uri)
    - [Variables de entorno faltantes](#variables-de-entorno-faltantes)
  - [Docker y Despliegue](#docker-y-despliegue)
    - [Contenedor se cierra inmediatamente](#contenedor-se-cierra-inmediatamente)
    - [Archivos estáticos no se visualizan](#archivos-estáticos-no-se-visualizan)
  - [Dependencias](#dependencias)
    - [Errores de Poetry](#errores-de-poetry)

## Base de Datos

### Error al conectar con PostgreSQL
Ocurre cuando el backend no puede alcanzar la base de datos, usualmente por credenciales incorrectas o porque el servicio no está activo.

> [!Note]
> Si usas Docker Compose, asegúrate de que el nombre del host sea el nombre del servicio definido en el `yml` (ej. `db` o `postgres`).

**Solución:**
1. Verificar que `PG_HOST` y `PG_PORT` sean correctos en el `.env`.
2. Comprobar que el servicio PostgreSQL esté corriendo:
   ```sh
   docker ps  # Si usas docker
   ```

### Migraciones pendientes
Si recibes errores de "table not found" o campos faltantes en la API.

**Solución:**
Ejecuta las migraciones manualmente para asegurar que el esquema esté actualizado:
```sh
python manage.py migrate
```

## Autenticación (Discord)

### Error `invalid_redirect_uri`
Este es el error más común al configurar el OAuth2 de Discord.

**Solución:**
Asegúrate de que la URL en `DISCORD_REDIRECT_URI` coincida **caracter por caracter** con la configurada en el portal de Discord. 
- Revisa si falta o sobra una barra diagonal `/` al final.
- Verifica si estás usando `http` en lugar de `https`.

### Variables de entorno faltantes
Si el login de Discord devuelve un error `500` o `NoneType`, puede que las variables no estén cargadas.

**Solución:**
Consulta el [manual de variables de entorno](./virtual-env.md) y asegúrate de que `DISCORD_CLIENT_ID` y `DISCORD_CLIENT_SECRET` estén presentes en tu `.env`.

## Docker y Despliegue

### Contenedor se cierra inmediatamente
Suele deberse a un error en el comando de inicio o falta de permisos.

**Solución:**
Revisa los logs del contenedor para identificar la causa:
```sh
docker logs <container>
```

### Archivos estáticos no se visualizan
Si el panel de administración de Django se ve sin estilos o faltan imágenes.

**Solución:**
Asegúrate de haber ejecutado el comando de recolección de estáticos:
```sh
python manage.py collectstatic --no-input
```
> [!Tip]
> El proyecto usa `whitenoise` para servir archivos estáticos, por lo que no es necesario un servidor Nginx adicional para este fin en despliegues simples.

## Dependencias

### Errores de Poetry
Si al ejecutar `poetry install` obtienes errores de resolución de dependencias.

**Solución:**
1. Intenta actualizar el lockfile:
   ```sh
   poetry lock --no-update
   ```
2. Asegúrate de estar usando Python 3.12 como se especifica en los [requerimientos](./onboarding.md).
