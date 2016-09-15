Solr
====

{% if vhost is defined %}
Every virtualhost on this system is configured to have it's own Solr-core. Each core is protected with it's own username and password so cores cannot interact with eachother.

Solr cores defined on this system:

{% for realm in vhost %}
{% if realm.db is defined %}
* Solr core: {{ realm.db }}  :  {{ realm.db }}:<password>@localhost:8983/solr/{{ realm.db }}

{% endif %}
{% endfor %}
{% endif %}
