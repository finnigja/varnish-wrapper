#install needed packages
sudo apt-get update
sudo apt-get install vim curl git build-essential libtool automake pkg-config python-docutils libncurses-dev libpcre3-dev libreadline-dev libev-dev libssl-dev flex bison -y

#symlink to scripts/configs that will be of use during testing
ln -s /vagrant ~/varnish-wrapper
