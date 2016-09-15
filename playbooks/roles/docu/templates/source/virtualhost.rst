Virtual webroot hosting
=======================

{% if vhost is defined %}
Virtual hosts configured on this system:

{% for url in vhost %}
* Virtualhost: {{ url.url }}

{% if url.alias is defined %}
  * Aliases: {{ url.alias|join(', ') }}
{% endif %}

  * Owner: {{ url.owner }}

{% if url.db is defined %}
  * Database: {{ url.db }}
{% endif %}

{% if url.ssl is defined %}
  * SSL Certificate: {{ url.ssl }}
{% endif %}

{% endfor %}

{% endif %}


