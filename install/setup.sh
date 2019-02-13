#!/bin/bash

sudo apt-get update;

# Python Setup
sudo apt-get install python -y;
sudo apt-get install python3 -y;
sudo apt-get install pip -y;
sudo apt-get install pip3 -y;
sudo apt-get install virutalenv -y;
sudo apt-get install python-dev -y;
sudo apt-get install python3-dev -y;

# Required Setup
sudo apt-get install build-essential -y;
sudo apt-get install libnetfilter-queue-dev -y;

# requirements
pip install scapy;
pip install scapy-http;
pip install netfilterqueue;

# Service Setup
# service apache2 start;
# service openvpn start;

# path = /var/www/html
