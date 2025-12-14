include .env
main: build up

build:
	docker compose $@

up:
	docker compose $@ -d
	docker exec -it ollama ollama run $(LLM_MODEL)

down:
	docker compose $@ -v

run:
	poetry run env $(shell cat .env) python3 src/srv.py
