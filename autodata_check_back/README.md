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
- Copy `./docker/.dockerenv.example` to `./docker/.dockerenv` and configure it.
- Взять файл autodata-f3395-e390064c90e9.json и добавить его в /project
- в .dockerenv изменить переменную GOOGLE_APPLICATION_CREDENTIALS=/app/autodata-f3395-e390064c90e9.json

```bash 
$ docker login your-registry (вводим логин пароль от своего gitlab пользователя)
$ docker-compose up -d
$ docker-compose exec app bash
$ ./manage.py collectstatic
$ ./manage.py migrate
```
