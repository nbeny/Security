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

import subprocess
import optparse
import re
from random import randint
import time


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
    while True:
        # print("\r[-] Current MAC = " + str(current_mac))
        if current_mac is not None:
            news_mac = mac_address_creator("")
            change_mac(options.interface, news_mac)
            current_mac = get_current_mac(options.interface)
            if current_mac == news_mac:
                print("[+] MAC address was successfully changed to " + current_mac)
                time.sleep(2)
                print("")
            else:
                print("[-] MAC address did not get changed.")
except KeyboardInterrupt:
    print("[-] Detected ctrl + C ... Quitting.")

