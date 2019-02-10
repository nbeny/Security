#!/usr/bin/env python

from netfilterqueue import NetfilterQueue
import socket


def print_and_accept(pkt):
    print(pkt)
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
# s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)
# print(s)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print("[-] Error run nfqueue.run_socket(s)")

# s.close()
nfqueue.unbind()
