FROM your-registry/templates/image/python:3-8-no-pip

RUN apt update -y && apt install -y ttf-dejavu

RUN pip install --no-cache-dir --upgrade pip setuptools==69.1.1 && pip install pipenv==2023.12.1
COPY project/Pipfile* /

COPY project/TimesNewRomanRegular.ttf /usr/share/fonts/
COPY project/TimesNewRomanCyr.ttf /usr/share/fonts/

RUN pipenv install --dev --deploy --system --ignore-pipfile

WORKDIR /app
COPY project /app
