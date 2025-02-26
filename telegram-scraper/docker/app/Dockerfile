FROM your-registry/templates/image/python:3-9-no-pip

RUN pip install --no-cache-dir --upgrade pip setuptools==67.8.0 && pip install pipenv==2023.5.19
COPY project/Pipfile* /

RUN pipenv install --dev --deploy --system --ignore-pipfile

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
COPY project /app
