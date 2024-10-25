migrate_up:
	alembic upgrade head

migrate_down:
	alembic downgrade -1

create_migration:
	alembic revision --autogenerate -m $(NAME)

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

.PHONY: create_migration migrate_up migrate_down up down build