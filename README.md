FIAAS "Full Install as a Service"
=================================

This is a collection of Ansible roles and playbooks to setup and configure a full LAMP stack on Debian with additional services like Varnish, Memcached or Redis where required. The FIAAS playbooks generate more than just the standard service on your VM.
FIAAS includes:
  * creation of users, vhosts, php-fpm pools, databases and solr cores
  * firewall and fail2ban enabled
  * monitoring with Icinga2
  * backups with Attic backup
  * automatic generation of Letsencrypt certificates with acme.sh
  * services are not left with default configuration values, but are dynamically resized according to the size of the VM.
  * PHP-FPM with worker mode Apache 2.4 and mod proxy fcgi for best performance
  * optional "extra" configs to configure those few annoying exceptions which can't be added in default roles
  * Vagrant examples for local development or playbook tests

Everything is currently built to run all services in one VM.

Environment setup
=================

Ansible = 2.1.1(.0) is used for this setup. (1.9.x still appears to work too)

  * sudo apt-get -y install python-dev libffi-dev libssl-dev python-virtualenv virtualenv
  * virtualenv ansible-2.1.1
  * source ansible-2.1.1/bin/activate
  * pip install ansible==2.1.1.0

Executing (vagrant)
===================

  * source ansible-2.1.1/bin/activate
  * cd vagrant/somevagrantsetup/
  * vagrant up --no-provision
  * provisioning:
    * OR: vagrant provision
    * OR: ansible-playbook -i inventory/ ../../playbooks/lamp.yml -u vagrant --ask-pass ( pass = vagrant )
    * OR: ./ansible-vagrant ../../playbooks/lamp.yml
  * Run the createresources.yml in a similar way


Executing
=========

```
$ source ansible-2.1.1/bin/activate
```

Assign 2 infra VMs in your inventory for monitoring and backups and run:
```
$ ansible-playbook -i inventory/production/ playbooks/infra-setup.yml
```

Create a LAMP VM:
```
$ ansible-playbook -i inventory/production/ playbooks/lamp.yml -l customer1
$ ansible-playbook -i inventory/production/ playbooks/createresources.yml -l customer1
$ ansible-playbook -i inventory/production/ playbooks/infra-client.yml -l customer1
```

The infra plays are optional, but without that you won't have monitoring and backups.

Host vars
=========

The configuration for a host allows to set plenty of options. There's not much hierarchy in the yaml because we found out it blocks flexibility.

An example host_vars file:

```
---
redis_required: True
varnish_required: True 
monitoring_over_ssh: True
solr_required: False
install_vsftpd: False
memcached_required: False

backup_required: True

vm_owner: devuser2

users:
  - name: devuser1
  - name: devuser2
  - name: devuser3

directories:
  - name: "/var/www/sites/www.vhost1.com"
    mode: "0755"
    delete: True
  - name: "/var/www/sites/www.vhost2.com"
    mode: "0755"
  - name: "/var/www/sites/www.vhost3.com"
    mode: "0755"

symlinks:
  - src: "/var/www/sites/www.vhost3.com"
    dest: "/var/www/sites/symlink"

databases:
  - name: vhost1db
    pass: vhost1pass
    delete: True
  - name: vhost2db
    pass: vhost2pass
  - name: vhost3db
    pass: vhost3pass
  - name: extern1
    user: extuser1
    pass: extpass1
    ip: "37.252.122.240"

phppools:
  - name: vhost1 
    pm: dynamic
    user: www-data
    group: www-data
    delete: True
  - name: vhost2
    user: www-data
    group: www-data
    pm: ondemand
  - name: vhost3 
    user: www-data
    group: www-data
    pm: ondemand

solr_cores:
  - name: vhost1
    pass: QuieC5eoFae7thus
  - name: vhost2
    pass: reTeech4ao7aGhai

vhosts:
  - url: "www.vhost1.com"
    basedir: "/var/www/sites/www.vhost1.com"
    admin: "admin@vhost1.com"
    alias: ['alias1.vhost1.com','alias2.vhost1.com']
    ssl: selfsigned
    ssl_redirect_http: True
    phppool: vhost1
    owner: devuser2
    delete: True
    monitoring: True
  - url: "www.vhost2.com"
    basedir: "/var/www/sites/www.vhost2.com"
    admin: "admin@vhost2.com"
    ssl: selfsigned
    alias: [ "alias.vhost2.com" ]
    phppool: vhost2
    owner: devuser2
    monitoring: False
  - url: "static.vhost3.com"
    basedir: "/var/www/sites/static.vhost3.com"
    admin: "admin@vhost3.com"
    ssl: letsencrypt
    ssl_redirect_http: True
    alias: ['alias1.vhost3.com','alias2.vhost3.com']
    phppool: vhost3
    owner: devuser1
    monitoring: True

extra_pkgs: []
php_extra_pkg: []
php_pecl_inactive_extensions: []
php_pecl_extra_extensions: []
```
Define a host in the inventory, create a similar host_vars file, run the lamp and createresources playbook against your VM and you'll be ready to go.
To delete something you created, set delete: True and use the deleteresources playbook to remove them. 

Support
=======
Feel free to open an issue or create a pull request in case you have questions or proposals to improve the project.

FiaasCo is available for commercial support and consultancy services to setup your own environment, add continuous deployments etc. Contact sales@fiaas.co or check https://www.fiaas.co for more information.

License
=======
This software is licensed under the terms of the MIT License, included in the COPYING file.

Authors
=======

Dieter Verhelst

Luc Stroobant
