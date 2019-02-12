# coding=utf-8                                                                  

"""                                                                             
    Security - Multiples offencives Tools                                       
    Copyright (C) 2018-2019 nbeny                                               
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
