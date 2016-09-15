General information
===================

Hello and welcome to the documentation. You are reading the documentation for {{ inventory_hostname }}. 
You should be connecting to the machine through {{ ansible_ssh_host }}.

{% if vhost == True %}
Vhosts configured on this system:

{% for url in vhost %}
* {{ url.url }}
  developer: {{ url.owner }}
{% endfor %}

{% endif %}
Enabled features on this server:

{% if redis_required == True %}* redis{% endif %}

{% if varnish_required == True %}* varnish{% endif %}

{% if memcached_required == True %}* memcached{% endif %}

{% if solr_required == True %}* solr{% endif %}

{% if install_vsftpd == True %}* ftp access{% endif %}


