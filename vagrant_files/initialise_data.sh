#!/usr/bin/env bash

cd /vagrant
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

workon xwing

python manage.py migrate
python manage.py bower install
python manage.py collectstatic
python manage.py load_xwing_data