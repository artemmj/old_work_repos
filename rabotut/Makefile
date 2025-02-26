nope:
	$(error Invalid target)

check-env-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi


# django
admin:
	docker-compose exec app ./manage.py createsuperuser

migrate:
	docker-compose exec app ./manage.py migrate

shell:
	docker-compose exec app ./manage.py shell

.PHONY: static
static:
	docker-compose exec app ./manage.py collectstatic

# pipenv
lock:
	docker-compose exec app pipenv lock -v

# docker
bash:
	docker-compose exec app bash

build:
	docker-compose build --build-arg DEBUG=True --no-cache

deploy:
	git pull && make restart
	docker-compose exec app ./manage.py migrate

down:
	docker-compose down

log:
	docker-compose logs -f --tail=100

restart:
	docker-compose restart app celery

stop:
	docker-compose stop

test:
	docker-compose exec app pytest

up:
	docker-compose up -d

flake8:
	docker-compose exec app flake8 --count

coverage:
	docker-compose exec app pytest --cov --cov-report=html --cov-report=term-missing:skip-covered
