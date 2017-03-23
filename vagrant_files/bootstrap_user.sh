#!/usr/bin/env bash

cd /home/vagrant
cp /vagrant/vagrant_files/.bashrc /home/vagrant/.bashrc
cp /vagrant/vagrant_files/.inputrc /home/vagrant/.inputrc
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv xwing -p $(which python3)
workon xwing
cd /vagrant
pip install -r requirements.txt
echo "xwing virtualenv created, make sure you install requirements"
byobu-enable

sudo service supervisor restart
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all
