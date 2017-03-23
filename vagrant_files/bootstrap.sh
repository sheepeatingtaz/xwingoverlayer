#!/usr/bin/env bash

apt-get update
apt-get install -q -y --force-yes python3 python git python-pip pkg-config redis-server redis-tools npm
apt-get install -q -y --force-yes python-dev supervisor build-essential python3-dev python-pip
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
