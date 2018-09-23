import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_users(host):
    user = host.user('owner1')
    assert user.exists
    assert user.home == '/home/owner1'
    user = host.user('devuser1')
    assert user.exists
    assert user.home == '/home/devuser1'
    user = host.user('devuser2')
    assert user.exists
    assert user.home == '/home/devuser2'
    user = host.user('devuser3')
    assert user.exists
    assert user.home == '/home/devuser3'
