.PHONY: api_prod
api_prod:
	@uvicorn src.main:app

.PHONY: api
api:
	@uvicorn src.main:app --reload

.PHONY: worker
worker:
	@celery -A src.celery_app worker --loglevel=info

.PHONY: run
run:
	@make worker & make api

.PHONY: run_prod
run_prod:
	@make worker & make api_dev

