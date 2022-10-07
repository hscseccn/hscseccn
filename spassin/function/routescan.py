'''
Function:
    路由器指纹识别
Author:
    spmonkey
邮箱：
    spmonkey@hscsec.cn
'''
# -*- coding: utf-8 -*-
import requests
from socket import *
from requests.packages.urllib3 import disable_warnings
disable_warnings()

def port_open(ip):
    if ':' not in ip:
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((ip, 80))
            s.shutdown(1)
            return ip
        except:
            return False
    else:
        return ip

def routescan(ip):
    ip = port_open(ip)
    if ip:
        if 'http' not in ip:
            ip = 'http://' + ip +'/'
        result = requests.get(ip, verify=False)
        result.encoding = 'utf-8'
        if '小米路由器' in result.text:
            print("Router Manufacturer is\033[1;34m 小米\033[0m.")
        elif 'ZTE Corporation. All Rights Reserved.' in result.text:
            print("Router Manufacturer is\033[1;34m 中兴\033[0m.")
        elif 'D-Link VoIP Wireless Router' in result.text:
            print("Router Manufacturer is\033[1;34m D-Link\033[0m.")
        elif 'Cisco Cable Modem' in result.text:
            print("Router Manufacturer is\033[1;34m Cisco\033[0m.")
        elif '乐视路由器' in result.text:
            print("Router Manufacturer is\033[1;34m 乐视\033[0m.")
        elif 'Wireless Broadband Router Management Console' in result.text:
            print("Router Manufacturer is\033[1;34m Verizon\033[0m.")
        elif '360家庭防火墙' in result.text:
            print("Router Manufacturer is\033[1;34m 360\033[0m.")
        else:
            print("未识别到厂商！")
    else:
        print(f"{ip}:80 is not open")

if __name__ == "__main__":
    setdefaulttimeout(1)
    url = input("Please enter the IP address or url: ")
    routescan(url)