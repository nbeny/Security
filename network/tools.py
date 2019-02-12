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

import os

def create_directory(data="data"):
    path = os.getcwd()
    path += "/" + data + "/"

    try:
        os.mkdir(path)
    except OSError:
        print("[-] Creation of the directory %s failed" % path)
    else:
        print("[+] Successfully created the directory %s" % path)


def add_in_file(data=None, file="None"):
    if data is None:
        return None
    
    path = os.getcwd()
    path += "/data/%s_spoof.txt" % file

    try:
        file = open(path, "a+")
        file.write(data)
        file.close()
    except OSError:
        print("[-] Creation of the file %s failed" % path)
