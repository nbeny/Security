#!/bin/bash

# shecker list
# iptables --list
# watch -n 0.1 iptables -L -v -n

# local
# iptables -I FORWARD -j NFQUEUE --queue-num 1

# Real word
iptables -I OUTPUT -d 10.0.2.0/24 -j NFQUEUE --queue-num 1
iptables -I INPUT -d 10.0.2.0/24 -j NFQUEUE --queue-num 1

# normal clear
# iptables --flush

# boosted clear
# iptables -P INPUT ACCEPT
# iptables -P FORWARD ACCEPT
# iptables -P OUTPUT ACCEPT
# iptables -t nat -F
# iptables -t mangle -F
# iptables -F
# iptables -X
