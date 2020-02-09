FIAAS "Full Install as a Service"
=================================

This is a collection of Ansible roles and playbooks to setup and configure a full LAMP stack on Debian with additional services like Varnish, Memcached or Redis where required. The FIAAS playbooks generate more than just the standard service on your VM.
FIAAS includes:
  * creation of users, vhosts, php-fpm pools, databases and solr cores
  * firewall and fail2ban enabled
  * monitoring with [Icinga2](https://www.icinga.org/)
  * backups with [Borg backup](https://github.com/borgbackup)
  * automatic generation of Letsencrypt certificates with [acme.sh](https://github.com/Neilpang/acme.sh)
  * services are not left with default configuration values, but are dynamically resized according to the size of the VM.
  * PHP-FPM with worker mode Apache 2.4 and mod proxy fcgi for best performance
  * Possible to use nginx to terminate ssl and enable http2 (default disabled, set nginx\_required: True)
  * optional "extra" configs to configure those few annoying exceptions which can't be added in default roles
  * Vagrant examples for local development or playbook tests

Everything is currently built to run all services in one VM.

Environment setup
=================

Ansible = 2.9 is required for this setup.

  * sudo apt-get -y install python-dev libffi-dev libssl-dev python-virtualenv virtualenv
  * virtualenv ansible-2.9.4
  * source ansible-2.9.4/bin/activate
  * pip install -r requirements.txt
  * ansible-galaxy install -r requirements.yml
  * ansible-galaxy collection install -r requirements.yml

Executing (vagrant)
===================

  * source ansible-2.9.4/bin/activate
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
$ source ansible-2.9.4/bin/activate
```

Assign the infra VMs in your inventory for monitoring and backups and run:
```
$ ansible-playbook -i inventory/production/ playbooks/icingaserver.yml
$ ansible-playbook -i inventory/production/ playbooks/backupserver.yml
$ ansible-playbook -i inventory/production/ playbooks/muninserver.yml
```
Debian Strech is the only supported version for the infra-servers (for the LAMP VMs Jessie is also still supported).

Create a LAMP VM:
```
$ ansible-playbook -i inventory/production/ playbooks/lamp.yml -l customer1
$ ansible-playbook -i inventory/production/ playbooks/createresources.yml -l customer1
$ ansible-playbook -i inventory/production/ playbooks/backup.yml -l customer1
$ ansible-playbook -i inventory/production/ playbooks/monitoring -l customer1
```

You can ommit the monitoring and backup plays if you need just the LAMP VM.

Host vars
=========

The configuration for a host allows to set plenty of options. There's not much hierarchy in the yaml because we found out it blocks flexibility.

An example host\_vars file:

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
  - name: /var/www/sites/www.vhost1.com
    mode: "0755"
    delete: True
  - name: /var/www/sites/www.vhost2.com
    mode: "0755"
  - name: /var/www/sites/www.vhost3.com
    mode: "0755"

symlinks:
  - src: /var/www/sites/www.vhost3.com
    dest: /var/www/sites/symlink

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
    ip:
      - 10.2.4.322

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
Define a host in the inventory, create a similar host\_vars file, copy the [group\_vars/all configuration from the vagrant inventory](https://github.com/FiaasCo/fiaas/tree/master/vagrant/vagrant/inventory/group_vars/all) and define your users, backup and monitoring settings which will apply to all systems.
run the lamp and createresources playbook against your VM and you'll be ready to go.
To delete something you created, set delete: True and use the deleteresources playbook to remove them. 

Important:
Always use a fully qualified domainname in your inventory when you define a server, the same fqdn will also be configured as the server hostname (`hostname -f`) if that's not already the case. Don't forget that a default "admin vhost" is added with the servername "{{ inventory\_hostname }}", so you won't be able to add an additional vhost with the fqdn of your server. Per default a Letsencrypt certificate will be requested for the server FQDN, if you are behind a firewall or run in vagrant, configure adminhost\_ssl and use selfsigned or commercial instead of letsencrypt.

Testing
=======
Molecule tests are being added.
Currently the project has Vagrant based Molecule tests in the createresources role. The box is prepared with the lamp playbook, so running the tests for this role can be considered as the integration test for the project. The tests will check if the resources are created and the main services are running after creation.
Run the tests with:
$ molecule test --scenario-name fiaas01
$ molecule test --scenario-name fiaas01-debian10
$ molecule test --scenario-name fiaas02-debian10

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
