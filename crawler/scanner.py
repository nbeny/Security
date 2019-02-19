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

import requests
import re
from urllib import parse

class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links

    def extract_links_form(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', response.content)

    def crawl(self, url=None):
        if url == None:
            url = self.target_url
        href_links = self.extract_links_form(url)
        for link in href_links:
            link = parse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                self.taget_links.append(link)
                print(link)
                crawl(link)

    def extract_forms(self, url):
        response = self.session.get(url)
        parse_html = BeautifulSoup(response.content)
        return parsed_html.findAll("form")

    def submit_for(self, form, value, url):
        action = form.get("action")
        post_url = urlparse.urljoin(url, action)
        # print(post_url)

        method = form.get("method")
        # print(method)

        inputs_list = form.findAll("input")
        post_data = {}
        for input in inputs_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value
            post_data[input_name] = input_name
        if method == "post":
            return self.session.post(post_url, data=post_data)
        return requests.post(post_url, parans=post_data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("[+] Testing form in " + link)

            if "=" in link:
                print("[+] Testing " + link)

    def test_xss_in_form(self, form, url):
        xss_test_script = "<script>alert('test')</script>"
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script in response.content
