import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_authorized_keys(host):
    with host.sudo():
        keyfile = host.file('/var/www/sites/svhost1/.ssh/authorized_keys')
        assert keyfile.exists
        assert keyfile.user == 'svhost1'
        assert keyfile.group == 'svhost1'
        assert keyfile.mode == 0o600
        assert keyfile.contains('ssh-rsa kieken ik@vhost1')
        assert keyfile.contains('ssh-rsa nogeenkieken gij@daar')
        keyfile = host.file('/var/www/sites/svhost3/.ssh/authorized_keys')
        assert keyfile.exists
        assert keyfile.user == 'svhost3'
        assert keyfile.group == 'svhost3'
        assert keyfile.mode == 0o600
        assert keyfile.contains('ssh-rsa kieken ik@vhost3')
