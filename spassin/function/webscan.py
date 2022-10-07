'''
Function:
    Web指纹识别
Author:
    spmonkey
博客链接:
    https://www.cnblogs.com/spmonkey/
邮箱：
    spmonkey@hscsec.cn
Github:
    https://github.com/spmonkey/
'''
# -*- coding:utf-8 -*-
import requests
import re
import socket
from qqwry import *
from bs4 import BeautifulSoup
import os
import sys
from .CMScan import CMScan
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from lib.get_user_agent import get_user_agent

class webscan:
    def __init__(self, url=None, proxies=None, thread=None, file_name=None):
        self.url = url
        self.thread = thread
        self.file_name = file_name
        if proxies != None:
            self.proxies = {
                "http": proxies,
                "https": proxies
            }
        else:
            self.proxies = proxies

    def webscan(self):
        num = 0
        if 'http' not in self.url:
            url = 'http://' + self.url + '/'
        else:
            url = self.url
        try:
            header = get_user_agent()
            result = requests.get(url, headers=header, proxies=self.proxies, verify=False)
            result.encoding = 'utf-8'
            result_re = re.compile("<title>(.*?)</title>")
            title = result_re.search(result.text).group(1)
            middleware_re = re.compile("(.*)")
            middleware = middleware_re.findall(result.headers['Server'])[0]
            if "/" in middleware:
                middleware_re = re.compile("(.*?)/")
                middleware = middleware_re.findall(middleware)[0]
                version_re = re.compile(f"{middleware}/(.*)")
                middleware_version = version_re.findall(result.headers['Server'])
            else:
                middleware = middleware
                middleware_version = []
            if middleware_version:
                middleware_version = middleware_version[0]
            else:
                middleware_version = '无法识别出目标中间件版本'
            system_re = re.compile("\((.*?)\)")
            system = system_re.findall(result.headers['Server'])
            if system:
                system = system[0]
            else:
                system = "无法识别出目标系统"
            development_re = re.compile("\) (.*?)/")
            development = development_re.findall(result.headers['Server'])
            if development:
                version_deve = re.compile(f"{development}/(.*)")
                development_version = version_deve.findall(result.headers['Server'])
                if development_version:
                    development_version = development_version[0]
                else:
                    pass
            else:
                pass
            cookie = result.cookies.items()
            print(f"Status     : {result.status_code} OK")
            print(f"Title      : {title}")
            print(f"Middleware : {middleware}")
            if self.file_name == None:
                pass
            else:
                cms = CMScan(url=self.url, thread=self.thread, file_name=self.file_name).CMScan_main()
            ips = self.CDNScan(self.url)
            if type(ips) == list:
                print("\n[ Attribution ]")
                for ip in range(len(ips)):
                    print(f"        IP         : \033[1;36m {ips[ip]}\033[0m")
                    print(f"        City       : \033[1;34m {self.home_location(ips[ip])[0]}\033[0m")
            else:
                    print(f"City       : {self.home_location(ips)[0]}")
            print("\nDetected Plugins:")
            print(f"""[ {middleware} ]
            Version  : \033[1;36m {middleware_version}\033[0m""")
            print(f"""[ System ]
            System   : \033[1;34m {system}\033[0m""")
            if development:
                print(f"""[ {development[0]} ]
                Version  : \033[1;36m {development_version}\033[0m""")
            else:
                pass
            print("""[ Cookies ]""")
            for name, value in cookie:
                print(f"            String   : \033[1;34m {name}\033[0m")       # "\033[1;34m 字体颜色：蓝色\033[0m"
            if "password" in result.text:
                soup = BeautifulSoup(result.content, "lxml")
                while True:
                    pass_type = soup.select("input")[num]['type']
                    if pass_type == "password":
                        pass_name = soup.select("input")[num]['name']
                        break
                    num += 1
                print("[ PasswordField ]")
                print(f"""        String   : \033[1;34m {pass_name}\033[0m""")
            print("HTTP Headers:")
            for header_name,header_value in result.headers.items():
                print(f"        {header_name}: {header_value}")
        except Exception as e:
            print(e)
        print("-------------------------------------")


    def CDNScan(self, url):
        number = 0
        ip_list = []
        if "http:" in url:
            url_http = re.compile("http://(.*?)/")
            domain = url_http.search(url).group(1)
        elif "https:" in url:
            url_http = re.compile("https://(.*?)/")
            domain = url_http.search(url).group(1)
        try:
            ips = socket.getaddrinfo(domain, 'http')
            for item in ips:
                if item[4][0] not in ip_list:
                    ip_list.append(item[4][0])
                    number += 1
            if number > 1:
                return ip_list
            else:
                return ip_list[0]
        except Exception as e:
            return f"[-] 请检查域名是否正确，报错信息：{e}"

    def home_location(self, ip):
        q = QQwry()
        try:
            update = updateQQwry(f'{path}\\function\\qqwry.dat')
            q.load_file(f'{path}\\library\\qqwry.dat')
            result = q.lookup(ip)
            return result
        except:
            return '无法查询到归属地'

