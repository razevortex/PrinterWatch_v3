#!/bin/bash

aptcheck() {
	if [dpkg -s "$1" &> /dev/null == 0 ]
		then
			echo install "$1"
			sudo apt install "$1"
			
		else
			echo "$1" is installed
	fi
	}

apps="apache2 libapache2-mod-wsgi-py3 python3-pip python3-venv python3-setuptools python3-wheel vim ufw"
pkgs="setuptools wheel bs4 pyotp Pillow qrcode requests django"

for app in $apps
do
	echo "$app"
	aptcheck "$app"
done

echo "Enter ServerName:"
read sn
snenv="$sn"env

python_setup() {
	cd /srv
	sudo python3 -m venv "$snenv"
	source "$sn"env/bin/activate
	for pkg in $pkgs
	do
		pip install "$pkg"
	done
	django-admin startproject "$sn"
	sed -i "s|.*ALLOWED_HOSTS.*|ALLOWED_HOSTS = ['$sn', '127.0.0.1']|" $sn/$sn/settings.py
}



grub_vm() {
    sed -i 's|.*GRUB_CMDLINE_LINUX_DEFAULT=.*|GRUB_CMDLINE_LINUX_DEFAULT="quiet splash video=hyperv_fb:1920x1080"|' /etc/default/grub
}

vhost_conf=("<VirtualHost *:80>"
"      	ServerAdmin admin@printerwatch"
"      	ServerName $sn" 
"	ServerAlias www.$sn"
"       DocumentRoot /srv/$sn"
"       ErrorLog /var/log/apache2/error.log"
"       CustomLog /var/log/apache2/access.log combined"
""
"       Alias /static /srv/$sn/static"
"       <Directory /srv/$sn/static>"
"               Require all granted"
"       </Directory>"
""
"       Alias /static /srv/$sn/media"
"       <Directory /srv/$sn/media>"
"               Require all granted"
"       </Directory>"
""
"       <Directory /srv/$sn/$sn>"
"               <Files wsgi.py>"
"                       Require all granted"
"               </Files>"
"       </Directory>"
""
"       WSGIDaemonProcess $sn python-path=/srv/$sn python-home=/srv/$snenv"
"       WSGIProcessGroup $sn"
"       WSGIScriptAlias / /srv/$sn/$sn/wsgi.py"
"</VirtualHost>")

apache2_conf=("<Directory /srv/>"
"        Options Indexes FollowSymLinks"
"        AllowOverride None"
"        Require all granted"
"</Directory>")

setup_apache() {
	sudo echo "" > "/etc/apache2/sites-available/$sn.config"

	for line in "${vhost_conf[@]}"
	do
		sudo echo "$line" >> "/etc/apache2/sites-available/$sn.config"
	done

	for line in "${apache_conf[@]}"
	do
		sudo echo "$line" >> "/etc/apache2/apache2.conf"
	done

	sudo a2ensite "$sn"
	sudo systemctl reload apache2
	sudo systemctl start apache2

	sudo echo "127.0.0.1 $sn" >> "/etc/hosts"
}
grub_vm
python_setup
setup_apache
