#clone, build, install, and configure Varnish as front-end cache (port 80)
cd
git clone https://github.com/varnishcache/varnish-cache.git
cd varnish-cache
./autogen.sh
./configure --prefix=/opt/varnish && make && sudo make install
cd
sudo cp -rv /vagrant/provision/skeleton/varnish/* /
sudo addgroup --system varnish
sudo adduser --system --disabled-login --no-create-home --ingroup varnish varnish
sudo adduser --system --disabled-login --no-create-home --ingroup varnish vcache
sudo adduser --system --disabled-login --no-create-home --ingroup varnish vlogger
sudo install -m 0600 /proc/sys/kernel/random/uuid /etc/varnish/secret
sudo service varnish start
