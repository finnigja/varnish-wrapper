# Varnish Cache Test Wrapper

Sometimes, it may be useful to be able to see how Varnish Cache modifies the
traffic that passes through it.

This Vagrant environment allows creation of a Varnish Cache test environment,
wrapping it with pre-/post-cache MITM capabilities.

This creates a single virtual machine running Ubuntu Trusty 14.04 with:
 - Varnish (front-end cache)
 - lighttpd (back-end content server)
 - Hitch (TLS termination)
 - mitmproxy (HTTP/HTTPS man-in-the-middle)

It should be fairly straightforward to swap out Varnish for some other cache
or proxy component, if a different target needs to be tested.


Tested with VirtualBox 5.0 and Vagrant 1.7.4.


## Standard Install

Varnish and Hitch are both pulled from their Github repositories and built
from source, in order to get most recent versions.

Initially, the configuration deployed is as follows:
```
  https-client  http-client
      |          |
  hitch:443      |
       \         |
         \       |
         varnish:80
             |
        lighttpd:8080
```


## MITM Monitor Mode

Scripts are provided to reconfigure into a pre- and post-cache MITM flow,
using mitmproxy running in reverse proxy mode:
```
  https-client  http-client
      |          |
  hitch:443      |
       \         |
         \       |
        mitmproxy:80
             |
         varnish:8081
             |
        mitmproxy:8082
             |
        lighttpd:8080
```

Running mitm-enable.sh will reconfigure Varnish, start a screen session, and
start mitmdump processes at both pre-cache and post-cache positions in the
flow.

The commands that are run to initialize the two mitmdump processes could be
modified, for example to run mitmproxy if the user wants interactive access
to the MITMed flows.

Running mitm-disable.sh will kill any mitmdump processes and reconfigure
Varnish to return the flow to original state.


## MITM Diff Mode

TBD - use header injection to tie pre-/post-cache requests to each other,
persist somewhere, and output diffs for each request that comes through the
cache.


## Logging

Logs for Hitch are dropped into the daemon syslog facility, which drop into
/var/log/daemon.log on the system.

Logs for Varnish can be accessed by executing /opt/varnish/bin/varnishlog,
which is documented at:
https://www.varnish-cache.org/docs/4.1/reference/varnishlog.html


## Author

https://twitter.com/chair6

