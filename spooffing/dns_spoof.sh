#!/bin/bash

# normal clear
iptables --flush -v

# shecker list
# iptables -L -nv
# watch -n 0.1 iptables -L -v -n

# local + Redirection Apache2
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -I ACCEPT -j NFQUEUE --queue-num 1 -v
iptables -I FORWARD -d 10.0.2.0/24 -j NFQUEUE --queue-num 1 -v

# Real word
iptables -I OUTPUT -d 10.0.2.0/24 -j NFQUEUE --queue-num 1 -v
iptables -I INPUT -d 10.0.2.0/24 -j NFQUEUE --queue-num 1 -v
iptables -A PREROUTING -t mangle -i eth0 -j NFQUEUE --queue-num 1 -v
iptables -I INPUT -s 10.0.2.1 -i eth0 -j NFQUEUE --queue-num 1 -v

# boosted clear
# iptables -P INPUT ACCEPT
# iptables -P FORWARD ACCEPT
# iptables -P OUTPUT ACCEPT
# iptables -t nat -F
# iptables -t mangle -F
# iptables -F
# iptables -X
