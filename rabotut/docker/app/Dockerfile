FROM your-registry/templates/image/python:3-11-no-pip

RUN pip install --no-cache-dir --upgrade pip setuptools==69.2.0 && pip install pipenv==2023.12.1
RUN mkdir /tmp/cert && wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" -O /tmp/cert/CA.pem
COPY project/Pipfile* /

RUN pipenv install --dev --deploy --system --ignore-pipfile

WORKDIR /app
COPY project /app

# fix broken python shell pasting
RUN echo "set enable-bracketed-paste off" >> ~/.inputrc
