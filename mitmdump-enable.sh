#!/bin/sh

#move varnish to 8081
sudo sed -i -e 's/VARNISH_LISTEN_PORT\=[[:digit:]]\+$/VARNISH_LISTEN_PORT\=8081/g' /etc/default/varnish
# point varnish to 8082
sudo sed -i -e 's/\.port \= \"[[:digit:]]\+"\;$/.port \= \"8082\"\;/g' /etc/varnish/default.vcl
sudo service varnish restart

