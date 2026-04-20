# ADR 0001 - Convenciones de API

Este documento define reglas simples para que la API se mantenga consistente y fácil de usar, tanto para quienes desarrollan como para quienes consumen los endpoints.

## Índice
- [ADR 0001 - Convenciones de API](#adr-0001---convenciones-de-api)
  - [Índice](#índice)
  - [Rutas y trailing slash](#rutas-y-trailing-slash)
  - [Formato de errores y exposición de detalles](#formato-de-errores-y-exposición-de-detalles)
  - [Autenticación en endpoints protegidos](#autenticación-en-endpoints-protegidos)

## Rutas y trailing slash

Para evitar diferencias entre endpoints y errores en clientes, todas las rutas se definen con `/` al final.

> Ejemplo
>
> `/api/health/`

Los endpoints que estén asociados a un modelo (CRUD), deben estar escritos en plural.

## Formato de errores y exposición de detalles

- En errores de cliente (4xx), se responde con mensajes cortos y claros para facilitar correcciones.
- En errores internos (5xx), se responde con un mensaje genérico y el detalle técnico se deja en logs.

## Autenticación en endpoints protegidos

- Los endpoints públicos se dejan solo para lectura cuando aplica.
- Los endpoints de escritura o sensibles requieren autenticación.
- El flujo OAuth de Discord usa `redirect_uri` fijo por entorno para evitar inconsistencias.
