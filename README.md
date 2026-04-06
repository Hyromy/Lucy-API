# Lucy API

API Restful para Lucy Project

![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-A30000?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-FF4438?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?logo=poetry&logoColor=white)

## Inicio Rápido

1. Clonar repositorio
   ```sh
   git clone https://github.com/Hyromy/Lucy.git    # https
   git clone git@github.com:Hyromy/Lucy.git        # ssh

   cd Lucy-API
   ```

2. Instalar dependencias
   ```sh
   poetry install
   poetry shell
   ```

3. Aplicar migraciones
   ```sh
   python manage.py migrate
   ```

4. Ejecutar servidor
   ```sh
   python manage.py runserver
   ```

## Documentación adicional
- [Manual de desarrollador](./docs/onboarding.md)
- [Manual de operaciones](./docs/runbook.md)
- [Problemas comunes](./docs/troubleshooting.md)
- [Variables de entorno](./docs/virtual-env.md)
