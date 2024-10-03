migrate_up:
	alembic upgrade head

migrate_down:
	alembic downgrade -1

create_migration:
	alembic revision --autogenerate -m $(NAME)

.PHONY: create_migration migrate_up migrate_down