.PHONY: up
up: ## alias docker-compose up -d
	docker-compose up -d

.PHONY: dev
dev: ## alias docker-compose up
	docker-compose up

.PHONY: install
install: ## alias docker-compose up -d --build
	docker-compose up -d --build

.PHONY: ps
ps: ## alias docker-compose ps
	docker-compose ps

.PHONY: stop
stop: ## alias docker-compose stop
	docker-compose stop

.PHONY: api
api: ## Attach a api container
	docker compose exec api bash

.PHONY: kvs
kvs: ## Attach a kvs container.
	docker compose exec kvs redis-cli

.PHONY: mongodb
mongodb: ## Attach a mongodb container.
	docker compose exec mongodb mongo -u root -proot

.PHONY: queue
queue: ## start a queue container.
	docker-compose run --rm consumer python consumer.py

.PHONY: test
test: ## start a all test.
	docker-compose run --rm api pytest

.PHONY: openapi
openapi: ## generate models from openapi. モデルディレクトリの横に一旦置いておく
	docker run --rm -v ${PWD}/app/docs/openapi.yaml:/app/docs/openapi.yaml -v ${PWD}/app/app/api/models:/app/docs/src/openapi_server/models openapitools/openapi-generator-cli generate -i ./app/docs/openapi.yaml -g python-fastapi -o /app/docs/ --global-property models --skip-validate-spec
