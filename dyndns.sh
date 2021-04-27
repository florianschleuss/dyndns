#!/bin/sh
# dyndns.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/dyndns-script
sudo python3 dyndns.py
cd /
