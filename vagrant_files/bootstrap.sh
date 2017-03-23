#!/usr/bin/env bash

apt-get update
apt-get install -q -y --force-yes screen htop vim curl wget
apt-get install -q -y --force-yes python3 python git python-pip pkg-config
apt-get install -q -y --force-yes python-dev htop supervisor build-essential
apt-get install -q -y --force-yes python3-dev freetds-dev python-imaging libjpeg8 libjpeg62-dev libfreetype6
apt-get install -q -y --force-yes libfreetype6-dev python-pip libxml2-dev libxmlsec1-dev libxslt1-dev zlib1g-dev
apt-get install -q -y --force-yes redis-server redis-tools npm
#apt-get upgrade -y
ln -s /usr/bin/nodejs /usr/bin/node
pip install virtualenvwrapper
npm install -g bower


mkdir /var/log/xwing
chown -R vagrant:vagrant /var/log/xwing

# Copy Redis Config
cp /vagrant/vagrant_files/redis.conf /etc/redis/redis.conf
service redis restart

# Copy Supervisor Files
cp /vagrant/vagrant_files/daphne.conf /etc/supervisor/conf.d/daphne.conf
cp /vagrant/vagrant_files/workers.conf /etc/supervisor/conf.d/workers.conf

# Update Supervisor & Start
# Make sure Supervisor comes up after a reboot.
systemctl enable supervisor
