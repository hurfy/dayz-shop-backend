.DEFAULT_GOAL := all


all: build down up

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

test:
	pytest

setup:
	pip install -r requirements.txt

lint:
	ruff check