import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_users(host):
    with host.sudo():
        user = host.user('devuser1')
        assert user.exists
        assert user.home == '/home/devuser1'
        user = host.user('svhost2')
        assert user.exists
        assert user.home == '/var/www/sites/svhost2'
        assert user.password == '$6$u6XLvPLf03a9Z$xgA3sWR6A1jOh10ExZZ/LrbOgojK2AgPsrKclJCLt7xoDpWuWPoGu6S4FRMuOki76eE9dUXgbPzcb0CMGyUVk/'
        user = host.user('svhost3')
        assert user.exists
        assert user.home == '/var/www/sites/svhost3'
        user = host.user('ftpuser')
        assert user.exists
        assert user.home == '/home/ftpuser'
        assert user.shell == '/bin/false'
        assert user.password == '$6$u6XLvPLf03a9Z$xgA3sWR6A1jOh10ExZZ/LrbOgojK2AgPsrKclJCLt7xoDpWuWPoGu6S4FRMuOki76eE9dUXgbPzcb0CMGyUVk/'
        user = host.user('vhostftpuser')
        assert user.exists
        assert user.home == '/var/www/sites/svhost3/private/vhostftpuser'
        assert user.shell == '/bin/false'
