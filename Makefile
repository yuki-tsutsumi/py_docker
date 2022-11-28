.PHONY: up
up: ## alias docker-compose up -d
	docker-compose up -d

.PHONY: ps
ps: ## alias docker-compose ps
	docker-compose ps

.PHONY: stop
stop: ## alias docker-compose stop
	docker-compose stop