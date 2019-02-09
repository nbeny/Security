#!/bin/bash

# local
iptables -I FORWARD -j NFQUEUE --queue-num 0

# Real word
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I INPUT -j NFQUEUE --queue-num 0

# normal clear
iptables --flush

# boosted clear
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
iptables -t nat -F
iptables -t mangle -F
iptables -F
iptables -X
