import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_apache_vhost_config(host):
    config = host.file('/etc/apache2/sites-available/www.svhost1.com.conf')
    assert config.exists
    assert config.contains('ServerName www.svhost1.com')
    assert config.contains('DocumentRoot /var/www/sites/svhost1/web')
    assert config.contains('fcgi://svhost1/')
    config = host.file('/etc/apache2/sites-available/www.svhost2.com.conf')
    assert config.exists
    assert config.contains('ServerName www.svhost2.com')
    assert config.contains('DocumentRoot /var/www/sites/svhost2/web')
    assert config.contains('fcgi://svhost2/')
    config = host.file('/etc/apache2/sites-available/www.svhost3.com.conf')
    assert config.exists
    assert config.contains('ServerName www.svhost3.com')
    assert config.contains('DocumentRoot /var/www/sites/svhost3/web')
    assert config.contains('fcgi://svhost3/')
    assert config.contains('alias1.svhost3.com')
    assert config.contains('alias2.svhost3.com')


def test_apache_vhost_enabled(host):
    link = host.file('/etc/apache2/sites-enabled/001-default.conf')
    assert link.exists
    assert link.is_symlink
    assert link.linked_to == '/etc/apache2/sites-available/www.svhost1.com.conf'
    link = host.file('/etc/apache2/sites-enabled/www.svhost2.com.conf')
    assert link.exists
    assert link.is_symlink
    assert link.linked_to == '/etc/apache2/sites-available/www.svhost2.com.conf'
    link = host.file('/etc/apache2/sites-enabled/www.svhost3.com.conf')
    assert link.exists
    assert link.is_symlink
    assert link.linked_to == '/etc/apache2/sites-available/www.svhost3.com.conf'
