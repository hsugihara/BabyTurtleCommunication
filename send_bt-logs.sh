#!/bin/bash

timestamp=$(date +%Y%m%d-%H%M%S)
folderName="bt_log-${timestamp}"


echo "archiving device logs into a file..."
# cwd=$PWD
# cd /home/nvidia/bt-01

# shellcheck disable=SC2086
tar -zcvf $folderName.tar.gz BT-log BT-log.*

# cd $cwd
# echo "archived into /home/nvidia/bt-01/$folderName.tar.gz"

echo "device logs collection completed!"

echo "send log file by email"

# set to_email
to_email=$1
# echo $to_email

python3 sendlog.py $folderName.tar.gz $to_email


echo "sent log file !"
echo "delete the log file "

rm $folderName.tar.gz

echo "deleted"

exit 0
