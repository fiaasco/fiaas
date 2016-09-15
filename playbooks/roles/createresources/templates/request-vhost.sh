#!/bin/bash

# acme request cert template for vhost {{ item.url }}
# This supposes you have a line in Drupal .htaccess that allows this type of requests
# https://www.drupal.org/node/2408321
# -  RewriteRule "(^|/)\." - [F]
# +  RewriteRule "(^|/)\.(?!well-known)" - [F]


/root/.acme.sh/acme.sh --issue --webroot {{ item.basedir }}/web -d {{ item.url }} {% if item.alias is defined %}{% for alias in item.alias %} -d {{ alias }} {% endfor %}{% endif %}

STATUS=$?

exit $STATUS
