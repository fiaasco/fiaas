import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pool_config(host):
    config = host.file('/etc/php/7.3/fpm/pool.d/vhost1.conf')
    assert config.exists
    assert config.contains('pm = dynamic')
    assert config.contains('user = www-data')
    assert config.contains('group = www-data')
    config = host.file('/etc/php/7.3/fpm/pool.d/vhost2.conf')
    assert config.exists
    assert config.contains('pm = ondemand')
    assert config.contains('user = www-data')
    assert config.contains('group = www-data')
    config = host.file('/etc/php/7.3/fpm/pool.d/vhost3.conf')
    assert config.exists
    assert config.contains('pm = ondemand')
    assert config.contains('user = www-data')
    assert config.contains('group = www-data')
