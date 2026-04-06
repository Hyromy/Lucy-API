> [!WARNING]
> Cambiar formato o aislar

El proyecto se ejecuta por defecto en modo desarrollo `PRODUCTION=False` con una configuración minima para funcionar.

Para configurar manualmente dichas variables, copia el archivo `.env.example` y pegalo en la raíz del proyecto como `.env`. A continuación se detallan las variables disponibles y su propósito:

- __`PRODUCTION`__: Define el modo de ejecución del proyecto.
- __`DJANGO_SECRET_KEY`__: Secret de seguridad para algo`...`.
- __`HOSTS`__: Hosts de algo `...` separados por coma (`,`).
- __`CORS_ALLOWED`__: Hosts de algo `...` separados por coma (`,`).
- __`CSRF_TRUSTED`__: Hosts de algo `...` separados por coma (`,`).
- __`PG_DB`__: Nombre de la base de datos PostgreSQL.
- __`PG_USER`__: Usuario de la base de datos PostgreSQL.
- __`PG_PASS`__: Contraseña de la base de datos PostgreSQL.
- __`PG_HOST`__: Host de la base de datos PostgreSQL.
- __`PG_PORT`__: Puerto de la base de datos PostgreSQL.
- __`DISCORD_CLIENT_ID`__: Identificador de aplicación de cliente discord. _Necesario para operaciones de [autenticación](../apps/_auth/)_.
- __`DISCORD_CLIENT_SECRET`__: Secret de seguridad de aplicación de cliente de discord. _Necesario para operaciones de [autenticación](../apps/_auth/)_.
- __`DISCORD_REDIRECT_URI`__: URL De redirección de autenticación de discord. _Debe de coincidir con la [url callback](../apps/_auth/urls.py)_. _Necesario para operaciones de [autenticación](../apps/_auth/)_.
