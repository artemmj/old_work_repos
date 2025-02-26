FROM your-registry/templates/image/python:3-8-no-pip

RUN apt install -y ttf-dejavu

RUN pip install --no-cache-dir --upgrade pip setuptools==49.2.1 && pip install pipenv==2021.5.29
COPY project/Pipfile* /

COPY project/TimesNewRomanRegular.ttf /usr/share/fonts/
COPY project/TimesNewRomanCyr.ttf /usr/share/fonts/

RUN pipenv install --dev --deploy --system --ignore-pipfile

WORKDIR /app
COPY project /app
