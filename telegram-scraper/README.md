# api - API

## How to install

```bash
$ cp docker/.dockerenv.example docker/.dockerenv
$ pip install pipenv
$ pipenv shell
$ cd project/ && pipenv install --dev --ignore-pipfile

'refer to this guide regarding pipenv interpreter in pycharm'
https://www.jetbrains.com/help/pycharm/pipenv.html#pipenv-new-project
```
in order to install dev dependencies run build with **--build-arg DEBUG=True**
## Run
Copy `./docker/.dockerenv.example` to `./docker/.dockerenv` and configure it.

```bash 
$ docker login your-registry (вводим логин пароль от своего gitlab пользователя)
$ make up
$ docker-compose exec app bash
$ ./manage.py collectstatic
$ ./manage.py migrate
```

## Инструкция по запуску сервиса

Идем на сервер
```
$ ssh work@api-prod-telegramscraper.your-site.pro
$ cd synapse-global/telegram-scraper/
```

Идем в контейнер
```
$ docker-compose exec app bash
$ ./manage.py shell
```

Дальше питон код, импортируем, запускаем сервис
```
$ from apps.channel.services import ParsingService
$ ParsingService().process()
```
