#!/usr/bin/env bash -x
python manage.py migrate
python manage.py bower install
python manage.py import_xwing_data
python manage.py clean_bower
python manage.py collectstatic --noinput
