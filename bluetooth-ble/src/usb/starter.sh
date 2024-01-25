# crontab -e
# @reboot /path/to/starter.sh
# use pip3
cd /home/pi
echo "running python"
sleep 10
echo "start" > /home/pi/python-input.log
sudo python3 ./input.py >> /home/pi/python-input.log
