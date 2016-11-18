#!/bin/bash

# copyfishtankpics.sh
#
# make to copy fishtank current pic and temp graph to webserver

# 2016 11 14
# 2016 11 16

eval $(ssh-agent)
cat /home/pi/.ssh/id_rsa | SSH_ASKPASS="/home/pi/.ssh/sshpassfile.sh" ssh-add -
# fuser -k /usr/bin/sshpass
# sshpass -f /home/pi/.ssh/sshpassfile scp /home/pi/fishtank/plot.png pi@pi3:/home/pi/fishtank/fishwww/
# sshpass -f /home/pi/.ssh/sshpassfile scp /run/shm/mjpeg/user_annotate.txt pi@pi3:/home/pi/fishtank/fishwww/
# sshpass -f /home/pi/.ssh/sshpassfile scp /run/shm/mjpeg/cam.jpg pi@pi3:/home/pi/fishtank/fishwww/
scp /home/pi/fishtank/plot.png pi@pi3:/home/pi/fishtank/fishwww/
scp /run/shm/mjpeg/user_annotate.txt pi@pi3:/home/pi/fishtank/fishwww/
scp /run/shm/mjpeg/cam.jpg pi@pi3:/home/pi/fishtank/fishwww/
ssh-add -D




