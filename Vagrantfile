Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "varnish-wrapper.local"
  #config.vm.network :forwarded_port, guest: 80, host: 8080
  config.vm.guest = :ubuntu

  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end

  config.vm.define :server do |server|
    server.vm.network :private_network, ip: "192.168.200.2", netmask: "255.255.255.0"
    server.vm.provision :shell, :privileged => false, :path => "provision/base.sh"
    server.vm.provision :shell, :privileged => false, :path => "provision/lighttpd.sh"
    server.vm.provision :shell, :privileged => false, :path => "provision/varnish.sh"
    server.vm.provision :shell, :privileged => false, :path => "provision/hitch.sh"
    server.vm.provision :shell, :privileged => false, :path => "provision/tools.sh"
    server.vm.provision :shell, :privileged => false, :path => "status.sh"
  end

end
