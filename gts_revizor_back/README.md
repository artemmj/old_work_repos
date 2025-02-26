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
$ make up
$ docker-compose exec app bash
$ ./manage.py collectstatic
$ ./manage.py migrate
```



# Развертывание для клиента

```
$ STAGE=(указываем dev или master)
$ wget -o https://dev-gts-revizor.website.yandexcloud.net/gts_revizor_back_${STAGE}.tar.gz
$ wget -o https://dev-gts-revizor.website.yandexcloud.net/gts_revizor_front_${STAGE}.tar.gz
$ docker load < gts_revizor_back_${STAGE}.tar.gz
$ docker load < gts_revizor_front_${STAGE}.tar.gz
$ docker-compose -f docker-compose-client.yml up -d
```
