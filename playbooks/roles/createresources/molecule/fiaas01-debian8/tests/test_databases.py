import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_databases(host):

    with host.sudo():
        # test if databases exist
        databases = host.run('mysql -u root -e "show databases"')
        assert 'vhost1db' in databases.stdout
        assert 'vhost2db' in databases.stdout
        assert 'vhost3db' in databases.stdout
        assert 'extern1' in databases.stdout

        # test users
        access = host.run('mysql -u vhost1db -pvhost1pass vhost1db \
          -e "SELECT user();"')
        assert access.rc == 0

        access = host.run('mysql -u vhost2db -pvhost2pass vhost2db \
          -e "SELECT user();"')
        assert access.rc == 0

        access = host.run('mysql -u vhost3db -pvhost3pass vhost3db \
          -e "SELECT user();"')
        assert access.rc == 0

        access = host.run('mysql -u extern1 -pextpass1 -e "SELECT user();"')
        assert access.rc == 0

        # test remote access grant
        access = host.run('mysql -u root -e "show grants for extern1;"')
        assert "'extern1'@'%'" in access.stdout
