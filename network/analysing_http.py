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

import netfilterqueue
import scapy.all as scapy


keywords = [
    "Accept-Encoding",
]


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum
   # del scapy_packet[scapy.TCP].len
    del scapy_packet[scapy.TCP].chksum
    return packet

def get_load(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        for keyword in keywords:
            if keyword in load:
                return load
    return None

def process_packet(packet):
    # print(packet)
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            accept_encoding = get_load(scapy_packet)
            if accept_encoding is not None:
                accept_encoding_print = """
                        >>>>>>>>>>><<<<<<<<<
                        [+] Accept-Encoding Found
                        {}
                        >>>>>>>>>>><<<<<<<<<
                """.format(accept_encoding)
                print(accept_encoding_print)
                
            # print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Responce")
            accept_encoding = get_load(scapy_packet)
            if accept_encoding is not None:
                accept_encoding_print = """
                        >>>>>>>>>>><<<<<<<<<
                        [+] Accept-Encoding Found
                        {}
                        >>>>>>>>>>><<<<<<<<<
                """.format(accept_encoding)
                print(accept_encoding_print)
            # print(scapy_packet.show())

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(1, process_packet)
queue.run()
