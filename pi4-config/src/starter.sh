# /etc/rc.local
# use pip3
cd /var/www/html/python/src
echo "running python"
echo "start" > /home/pi/python-bgdeploy.log
sudo python3 ./bgDeployment.py >> /home/pi/python-bgdeploy.log
