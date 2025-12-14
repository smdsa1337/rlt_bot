include .env
main: build up

build:
	docker compose $@

up:
	docker compose $@ -d
	docker exec -it rlt_bot-ollama-1 ollama run $(LLM_MODEL)

down:
	docker compose $@ -v

run:
	poetry run env $(shell cat .env) python3 src/srv.py
