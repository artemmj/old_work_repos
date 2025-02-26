#!/usr/bin/env sh

celery -A apps worker -l info -B -c 4
