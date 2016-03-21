#!/bin/sh

psgrep() { ps up $(pgrep -f $@) 2>&-; }

psgrep lighttpd
psgrep hitch
psgrep varnish

sudo netstat -tlp
