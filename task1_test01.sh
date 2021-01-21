#!/bin/bash

#Create a bash script that sets up the following system properties on Ubuntu 18.04 server:

#    Time zone
#    Locale
#    Move sshd to listen port 2498 instead of 22
#    Deny remote login as root user
#    Add the serviceuser account to system
#    Grant sudo rights to the serviceuser
#    Limit serviceuser sudo rights to start|stop|restart services
#    Deploy Nginx server and make it autostart on reboot
#    Deploy Monit server and make it autostart on reboot
#    Set Nginx to proxy requests to the Monit server with the basic auth using devops/test credentials.

 set -e
 #set -x


while [[ `ps aux | grep -i apt | wc -l` != 1 ]] ; do
    echo 'apt is locked by another process.'
    sleep 15
    ps aux | grep -i apt | wc -l
done

echo 'apt is free. Let`s continue.'

echo $'\n'


echo "------Set time------"
region=Europe
city=Moscow

RESULT=`timedatectl | grep "Time zone" | awk '{print $3}'`

if [[ $RESULT == $region/$city ]]
then
   echo 'Timezone is correct'
else
   echo 'Changing timezone.'
   rm -rf /etc/localtime
   ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime
   echo 'Timezone is correct'
fi

echo "------Set locale------"
locale=en_US.UTF-8
lc=C.UTF-8

RESULT=`locale | grep LC_ALL=$lc`
if [[ "$RESULT" == "LC_ALL=$lc" ]] ; then
    echo 'Locale is set already.'
else
    locale-gen $locale
    update-locale LC_ALL=$lc
    update-locale LANGUAGE=$lc
    echo 'Locale is set. User must logout and login or reboot system.'
fi
echo "------Finish setting locale------"

echo "------Change ssh port and set root login deny------"
old_ssh=22
new_ssh=2498

RESULT=$((`ss -tln | grep ":$old_ssh" | wc -l`))

if [[ $RESULT -gt 0 ]]
then
   echo 'SSH server is working'
   echo 'Changing SSH port'
   sed -i "s/^.*Port[[:space:]][0-9]\+/Port $new_ssh/" /etc/ssh/sshd_config
   sed -i 's/^.*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
   echo 'Restart sshd'
   systemctl sshd restart
   echo "SSH server now listen at port $new_ssh"
else
    echo 'Installing sshd........'
    apt update
    apt upgrade -y
    apt install -y openssh-server
    sed -i "s/^.*Port[[:space:]][0-9]\+/Port $new_ssh/" /etc/ssh/sshd_config
    sed -i 's/^.*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
    echo 'Restart sshd'
    systemctl restart sshd
    echo "SSH server now listen at port $new_ssh"
fi

echo "------Finish setting ssh port and root permissions------"

echo "------Create serviceuser------"
username=serviceuser

RESULT = $((cat /etc/passwd | grep -w sshd | wc -l))

if [[ $RESULT -ne 0]]
then
    echo 'User already exist'
else
    useradd  -m -p $(openssl passwd -1 serviceuser) -s /bin/bash $username
    usermode -aG sudo $username
    echo "$username ALL=NOPASSWD:/bin/systemctl" >> /etc/sudoer
fi
echo "------serviceuser created------"

echo "------Deploy NGINX------"
package=nginx
if systemctl is-active --quiet $package
then
    echo "Nginx already installed"
else
    apt install $package
    systemctl start $package
    systemctl enable $package
fi
echo "------NGINX deployed------"

echo "------Deploy Monit------"
package=monit
if systemctl is-active --quiet $package
then
    echo "Monit already installed"
else
    apt install $package
    systemctl start $package
    systemctl enable $package
fi

echo "------Monit deployed------"

echo "------Enable NGINX work as proxy to monit------"
cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.back
unlink /etc/nginx/sites-available/default
echo \
    'server {
        listen 80;

        location / {
            proxy_pass http://127.0.0.1:2812;
            proxy_set_header Host $host;
        }
    }' > /etc/nginx/sites-available/proxy
ln -s /etc/nginx/sites-available/proxy /etc/nginx/sites-enabled/proxy
nginx -s reload
sed -i 's/# set httpd/set httpd/i; s/#     use address localhost/use address localhost/i; s/#     allow localhost/allow localhost/i; s/#     allow admin:monit/allow devops:test/i' /etc/monit/monitrc
    echo \
        'check process nginx with pidfile /var/run/nginx.pid
            start program = "/etc/init.d/nginx start"
            stop program = "/etc/init.d/nginx stop"' >> /etc/monit/monitrc
monit reload


RESULT=`ufw status | grep Status: |awk '{print $2}'`
if [[ "$RESULT" == "active" ]] ; then
    echo 'UFW is start and configured already.'
else
    ufw --force enable
    ufw allow 2498
    ufw allow http
    ufw default deny incoming
    ufw default allow outgoing
    echo 'UFW is configured.'
fi
echo "------UFW configured------"