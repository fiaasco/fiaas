#!/bin/bash

# acme request cert template for vhost {{ item.url }}

/root/.acme.sh/acme.sh --issue --webroot /var/www/acme -d {{ item.url }} {% if item.alias is defined %}{% for alias in item.alias %} -d {{ alias }} {% endfor %}{% endif %}

STATUS=$?

exit $STATUS
