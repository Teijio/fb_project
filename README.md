# fb_project

command: sh -c "alembic upgrade head"
localhost for local
fb_postgresql for prod

при локальной в .env подключение к БД через localhost
prod - по имени контейнера fb_postgresql

docker build -t ridpfrep/fb_project:latest .
docker push ridpfrep/fb_project:latest

# сгенерировать новую миграцию
alembic revision --autogenerate -m "name" --rev-id 02 