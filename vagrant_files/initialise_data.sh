#!/usr/bin/env bash

cd /vagrant
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

workon xwing

python manage.py post_deploy