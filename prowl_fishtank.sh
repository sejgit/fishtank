#! /bin/bash
# Script by aus
# Requirements: curl
# Usage: ./prowl.sh priority(-2 to 2) appname description
# Example: ./prowl.sh 0 "hello world" "this is only a test"
# modified for two api's by sej 05 07 2016

app="Raspi Fishtank"
priority=$1
eventname=$2
description=$3
apikey1=478f1343324309aeaa764704ebc8b2988dc7ec3b # sej key
apikey2=779712cfa1b032186987d45d481914e42a50c50e # tej key
if [ $# -ne 3 ]; then
	echo "prowl"
	echo "Usage: ./prowl.sh priority(-2 to 2) appname description"
	echo 'Example: ./prowl.sh 0 "linux" "this is a test"'
else
    curl https://prowl.weks.net/publicapi/add -F apikey=$apikey1 -F priority=$priority -F application="$app" -F event="$eventname" -F description="$description"
    curl https://prowl.weks.net/publicapi/add -F apikey=$apikey2 -F priority=$priority -F application="$app" -F event="$eventname" -F description="$description"
fi

