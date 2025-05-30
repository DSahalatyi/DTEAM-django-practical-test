#!/bin/sh

python manage.py migrate
RUN python manage.py collectstatic --noinput