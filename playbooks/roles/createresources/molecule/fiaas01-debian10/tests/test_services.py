import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_services(host):
    service = host.service('apache2')
    assert service.is_running
    service = host.service('varnish')
    assert service.is_running
    service = host.service('solr')
    assert service.is_running
    service = host.service('mariadb')
    assert service.is_running
