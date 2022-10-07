'''
Function:
    CDN查询
Author:
    spmonkey
邮箱：
    spmonkey@hscsec.cn
'''
# -*- coding: utf-8 -*-
import socket
import json

class CDN:
    def __init__(self, domain=None):
        self.ip_list = []
        self.domain = domain

    def CDNScan(self):
        number = 0
        try:
            ips = socket.getaddrinfo(self.domain, 'http')
            for item in ips:
                if item[4][0] not in self.ip_list:
                    self.ip_list.append(item[4][0])
                    number += 1
            if number > 1:
                print(f"[+] {self.domain} 存在CDN")
                return self.ip_list
            else:
                return f"[-] {self.domain} 不存在CDN，ip为 {self.ip_list[0]}"
        except Exception as e:
            return f"[-] 请检查域名是否正确，报错信息：{e}"

