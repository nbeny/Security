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
