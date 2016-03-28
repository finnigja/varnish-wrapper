#clone, build, install and configure Hitch for TLS termination (port 443)
cd
git clone https://github.com/varnish/hitch.git
cd hitch
./bootstrap
./configure --prefix=/opt/hitch && make && sudo make install
cd
sudo cp -rv /vagrant/provision/skeleton/hitch/* /
sudo addgroup --system hitch
sudo adduser --system --disabled-login --no-create-home --ingroup hitch hitch
cd /etc/hitch/certs
sudo openssl genrsa -out varnish-wrapper.local.key 2048 > /dev/null
sudo openssl req -new -x509 -key varnish-wrapper.local.key -out varnish-wrapper.local.cert -days 3650 -subj /CN=varnish-wrapper.local
cat varnish-wrapper.local.key varnish-wrapper.local.cert | sudo tee varnish-wrapper.local.pem > /dev/null
cd
sudo service hitch start
