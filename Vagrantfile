# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    config.vm.hostname = "xwing"
    config.vm.box = "bento/ubuntu-16.04"
    config.vm.provision :shell, path: "vagrant_files/bootstrap.sh"
    config.vm.provision :shell, path: "vagrant_files/bootstrap_user.sh", privileged: false
    config.vm.network "public_network"
    config.vm.network :forwarded_port, guest: 6379, host: 6380 # redis
    config.vm.network :forwarded_port, guest: 8008, host: 8008 # system
    config.vm.provision :shell, path: "vagrant_files/initialise_data.sh", privileged: false
    config.vm.provision :shell, run: "always", :inline => "sudo service supervisor restart"
end
