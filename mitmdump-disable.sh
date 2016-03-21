#!/bin/sh

sudo killall mitmdump

#move varnish to 80
sudo sed -i -e 's/VARNISH_LISTEN_PORT\=[[:digit:]]\+/VARNISH_LISTEN_PORT\=80/g' /etc/default/varnish
# point varnish to 8080
sudo sed -i -e 's/\.port \= \"[[:digit:]]\+"\;$/.port \= \"8080\"\;/g' /etc/varnish/default.vcl
sudo service varnish restart
