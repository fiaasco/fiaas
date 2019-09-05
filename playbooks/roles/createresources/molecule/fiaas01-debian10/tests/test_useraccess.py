import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_authorized_keys(host):
    with host.sudo():
        keyfile = host.file('/home/devuser1/.ssh/authorized_keys')
        assert keyfile.exists
        assert keyfile.user == 'devuser1'
        assert keyfile.group == 'devuser1'
        assert keyfile.mode == 0o600
        assert keyfile.contains('ssh-rsa key devuser1@vagrant')
