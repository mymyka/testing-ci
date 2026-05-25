.PHONY: install migrate upgrade downgrade revision history current heads merge-heads

install:
	uv sync

ALEMBIC = uv run alembic -c migrations/alembic.ini

migrate:
	$(ALEMBIC) upgrade head

upgrade:
	$(ALEMBIC) upgrade $(rev)

downgrade:
	$(ALEMBIC) downgrade $(rev)

revision:
	$(ALEMBIC) revision --autogenerate -m "$(msg)"

history:
	$(ALEMBIC) history --verbose

current:
	$(ALEMBIC) current

heads:
	$(ALEMBIC) heads

merge-heads:
	$(ALEMBIC) merge -m "$(msg)" $(shell $(ALEMBIC) heads | awk '{print $$1}' | tr '\n' ' ')
