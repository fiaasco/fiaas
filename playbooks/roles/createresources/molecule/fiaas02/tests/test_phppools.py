import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pool_config(host):
    config = host.file('/etc/php/7.0/fpm/pool.d/svhost1.conf')
    assert config.exists
    assert config.contains('pm = dynamic')
    assert config.contains('user = svhost1')
    assert config.contains('group = svhost1')
    config = host.file('/etc/php/7.0/fpm/pool.d/svhost2.conf')
    assert config.exists
    assert config.contains('pm = ondemand')
    assert config.contains('user = svhost2')
    assert config.contains('group = svhost2')
    config = host.file('/etc/php/7.1/fpm/pool.d/svhost3.conf')
    assert config.exists
    assert config.contains('pm = dynamic')
    assert config.contains('user = svhost3')
    assert config.contains('group = svhost3')
