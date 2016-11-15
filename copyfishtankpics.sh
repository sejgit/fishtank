#!/bin/bash

# copyfishtankpics.sh
#
# make to copy fishtank current pic and temp graph to webserver

# 2016 11 14

sshpass -f /home/pi/.ssh/sshpass scp /home/pi/fishtank/plot.png pi@pi3:/home/pi/fishdata/
sshpass -f /home/pi/.ssh/sshpass scp /run/shm/mjpeg/user_annotate.txt pi@pi3:/home/pi/fishdata/
sshpass -f /home/pi/.ssh/sshpass scp /run/shm/mjpeg/cam.jpg pi@pi3:/home/pi/fishdata/




