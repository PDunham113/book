# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/jammy64"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  config.vm.network "forwarded_port", guest: 3306, host: 3306

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    MYSQL_LIB_URL=https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb
    MYSQL_LIB=/tmp/mysql_apt_config.deb

    export DEBIAN_FRONTEND=noninteractive

    apt update
    apt install -y debconf-utils

    debconf-set-selections
    echo 'mysql-apt-config mysql-apt-config/repo-codename select jammy' > debconf-set-selections
    echo 'mysql-apt-config	mysql-apt-config/select-server	select	mysql-8.0' > debconf-set-selections
    echo 'mysql-apt-config	mysql-apt-config/repo-distro	select	ubuntu' > debconf-set-selections
    echo 'mysql-apt-config	mysql-apt-config/select-tools	select	Enabled' > debconf-set-selections
    echo 'mysql-apt-config	mysql-apt-config/select-product	select	Ok' > debconf-set-selections
    echo 'mysql-apt-config	mysql-apt-config/repo-url	string	http://repo.mysql.com/apt' > debconf-set-selections
    echo 'mysql-apt-config	mysql-apt-config/unsupported-platform	select	abort' > debconf-set-selections
    echo 'mysql-apt-config	mysql-apt-config/select-preview	select	Disabled' > debconf-set-selections
    echo 'mysql-apt-config	mysql-apt-config/preview-component	string	' > debconf-set-selections
    echo 'mysql-apt-config	mysql-apt-config/tools-component	string	mysql-tools' > debconf-set-selections
    echo 'mysql-community-server	mysql-community-server/root-pass	password	' > debconf-set-selections
    echo 'mysql-community-server	mysql-community-server/re-root-pass	password	' > debconf-set-selections
    echo 'mysql-community-server	mysql-community-server/data-dir	note	' > debconf-set-selections
    echo 'mysql-community-server	mysql-server/default-auth-override	select	Use Strong Password Encryption (RECOMMENDED)' > debconf-set-selections
    echo 'mysql-community-server	mysql-community-server/remove-data-dir	boolean	false' > debconf-set-selections
    echo 'mysql-community-server	mysql-community-server/root-pass-mismatch	error	' > debconf-set-selections
    echo 'mysql-community-server	mysql-server/lowercase-table-names	select	' > debconf-set-selections

    wget -q $MYSQL_LIB_URL -O $MYSQL_LIB
    apt install $MYSQL_LIB
    apt update
    apt install -y mysql-server

    # Create a password-enabled user & give them all permissions
    # TODO: Explicitly give them what they need for migration management
    mysql -e 'CREATE USER `vagrant`@`%` IDENTIFIED BY `vagrant`;'
    mysql -e 'GRANT ALL ON *.* TO `vagrant`@`%`;'

    apt-get update
    apt-get install \
      python3 \
      python3-pip \
    -y

    yes | python3 -m pip install \
        git+https://github.com/PDunham113/jaunt.git \
        mysql-connector-python
  SHELL
end
