FROM your-registry/templates/image/python:3-8-no-pip

RUN pip install --no-cache-dir --upgrade pip setuptools==49.2.1 && pip install pipenv==2021.5.29
COPY project/Pipfile* /

RUN pipenv install --dev --deploy --system --ignore-pipfile

WORKDIR /app
COPY project .
