#!/bin/bash
# connectfishwww.sh
# used to connect or reconnect fishwww directory from pi3 to bickpi
# 2016 07 18

fusermount -u /home/pi/fishwww
sshfs -o reconnect -o follow_symlinks -o allow_other pi@10.0.1.14:/var/www/html/ /home/pi/fishwww
