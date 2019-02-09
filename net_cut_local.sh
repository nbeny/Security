#!/bin/bash

iptables -I OUTPUT -j NFQUEUE --queue-num 0
