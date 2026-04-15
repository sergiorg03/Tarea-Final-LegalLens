## Levantar el contenedor
docker compose up -d --build

## Ejecutar las migraciones en la BD
docker compose exec app_django python /app/app_django/manage.py migrate