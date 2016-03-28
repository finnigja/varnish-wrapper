#start with lighttpd as content back-end (port 8080)
sudo apt-get install lighttpd -y
sudo sed -i -e 's/= 80$/= 8080/g' /etc/lighttpd/lighttpd.conf
sudo service lighttpd restart
service lighttpd status
