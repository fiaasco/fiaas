import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_solrcores(host):
    core_config = \
      host.file("/opt/solr/multicore/solr/vhost1core/conf/solrconfig.xml")
    assert core_config.exists

    core_curl = host.run('curl --user vhost1core:QuieC5eoFae7thus \
                         http://localhost:8983/solr/vhost1core/admin/ping')
    assert '<str name="status">OK</str>' in core_curl.stdout
    assert '403' not in core_curl.stdout
    assert '404' not in core_curl.stdout

    core_config = host.file('/opt/solr/multicore/solr/vhost2core/conf/solrconfig.xml')
    assert core_config.exists

    core_curl = host.run('curl --user "vhost2core:reTeech4ao7aGhai" \
                          http://localhost:8983/solr/vhost2core/admin/ping')
    assert '<str name="status">OK</str>' in core_curl.stdout
    assert '403' not in core_curl.stdout
    assert '404' not in core_curl.stdout
