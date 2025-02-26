#!/usr/bin/env sh

gunicorn --bind 0.0.0.0:8000 --timeout 600 --log-level debug --access-logfile - --access-logformat '%({X-Request-Id}i)s \"%(r)s\" %(s)s \"%(a)s\"' --reload --workers 4 --limit-request-line 8190 apps.wsgi:application
