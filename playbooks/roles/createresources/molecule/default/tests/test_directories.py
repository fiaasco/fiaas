import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directories(host):
  directory = host.file('/var/www/sites/svhost1')
  assert directory.exists
  assert directory.is_directory
  assert directory.user == 'svhost1'
  assert directory.group == 'svhost1'
  assert directory.mode == 0o775
  directory = host.file('/var/www/sites/svhost2')
  assert directory.exists
  assert directory.is_directory
  assert directory.user == 'svhost2'
  assert directory.group == 'svhost2'
  assert directory.mode == 0o771
  directory = host.file('/var/www/sites/svhost3')
  assert directory.exists
  assert directory.is_directory
  assert directory.user == 'svhost3'
  assert directory.group == 'svhost3'
  assert directory.mode == 0o770
  directory = host.file('/home/ftpuser')
  assert directory.exists
  assert directory.is_directory
  assert directory.user == 'ftpuser'
  assert directory.group == 'devuser1'
  assert directory.mode == 0o775
#  directory = host.file('/var/www/sites/svhost3/private/vhostftpuser')
#  assert directory.exists
#  assert directory.is_directory
#  assert directory.user == 'vhostftpuser'
#  assert directory.group == 'devuser3'
#  assert directory.mode == 0o775
