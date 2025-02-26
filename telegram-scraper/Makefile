nope:
	$(error Invalid target)

check-env-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

admin:
	docker-compose exec app ./manage.py createsuperuser

bash:
	docker-compose exec app bash

build:
	docker-compose build --build-arg DEBUG=True

deploy:
	git pull && make restart
	docker-compose exec app ./manage.py migrate

down:
	docker-compose down

log:
	docker-compose logs -f --tail 100 app celery redis db nginx

migrate:
	docker-compose exec app make migrate

restart:
	docker-compose -f docker-compose.yml restart app celery

shell:
	docker-compose exec app ./manage.py shell

stop:
	docker-compose stop

test:
	docker-compose exec app pytest -s

up:
	docker-compose -f docker-compose.yml up -d
