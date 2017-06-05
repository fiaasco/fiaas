# PHP 5.6 for Debian Stretch

This role contains a minimal implementation of PHP 5.6 FPM for Debian Stretch servers. It's mainly aimed to allower easier upgrades to Stretch and comes with only one php-fpm pool configured (so not all the pool options in create- and removeresources are available).
To use this PHP 5.6 pool, specify ```phppool: php56``` in your vhost.
