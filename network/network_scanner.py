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

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    options = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\t MAC Address\n-----------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


try:
    options = get_arguments()
    scan_result = scan(options.target)
    print_result(scan_result)
except KeyboardInterrupt:
    print("[-] Detected ctrl + C ... Quitting.")
