#!/bin/bash
# connectfishwww.sh
# used to connect or reconnect fishwww directory from pi3 to bickpi
# 2016 07 18

function error_exit
{
    echo "$1" 1>&2
    exit 1
}

# Using error_exit

ls ~/fishwww
if [ "$?" = "0" ]
    then
        error_exit "fishwww all ok"
    else
        fusermount -u /home/pi/fishwww
        sshfs -o reconnect -o follow_symlinks -o allow_other pi@10.0.1.14:/var/www/html/ /home/pi/fishwww
        error_exit "fishwww not connected. reconnecting"
fi


