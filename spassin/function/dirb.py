'''
Function:
    目录爆破
Author:
    spmonkey & FhoeniX42S
博客链接:
    https://www.cnblogs.com/spmonkey/
邮箱：
    spmonkey@hscsec.cn
Github:
    https://github.com/spmonkey/
'''
# -*- coding:utf-8 -*
import requests
import queue
import threading
import time
import os
import sys
from urllib.parse import quote
from requests.packages.urllib3 import disable_warnings
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
disable_warnings()


class directory:
    def __init__(self, url=None, file_name=None, thread=None, proxies=None):
        self.q = queue.Queue()
        self.__stop = 0
        self.url = url
        self.file_name = file_name
        self.thread = thread
        self.lock = threading.Lock()
        if proxies != None:
            self.proxies = {
                "http": proxies,
                "https": proxies
            }
        else:
            self.proxies = proxies

    def file_storage(self):
        files = open(f"{self.file_name}", "r").readlines()
        for file in files:
            path = file.strip("\n")
            self.q.put(path)

    def dirb(self):
        while self.lock:
            try:
                if self.q.qsize() == 0:
                    self.__stop += 1
                    break
                elif self.q.get():
                    url = self.url + quote(self.q.get())
                    print(f"\r{url}", end="")
                    headers = {'User-Agent': 'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)'}
                    result = requests.get(url=url, headers=headers, proxies=self.proxies, verify=False, timeout=5)
                    if result.status_code < 400:
                        print(f"\r[{result.status_code}] => {url}", file=open(f"{path}\output\dirurl.txt", "a+"))
                else:
                    url = self.url
                    print(f"\r{url}", end="")
                    headers = {
                        'User-Agent': 'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)'}
                    result = requests.get(url=url, headers=headers, proxies=self.proxies, verify=False, timeout=5)
                    if result.status_code < 400:
                        print(f"\r[{result.status_code}] => {url}", file=open(f"{path}\output\dirurl.txt", "a+"))
            except:
                pass

    def main(self):
        self.file_storage()
        t_list = []
        if not os.path.exists(path):
            os.makedirs(f"{path}\output")
        if os.path.exists(f"{path}\output\dirurl.txt"):
            os.remove(f"{path}\output\dirurl.txt")
        print(f"已启用的线程数：{self.thread}")
        for i in range(self.thread):
            t = threading.Thread(target=self.dirb, args=())
            t.daemon = 1
            t_list.append(t)
        for j in t_list:
            j.start()
        while 1:
            if self.__stop == 1:
                break
        print(" ")
        print(f"\n\rScan is Over! 请前往{path}\output\dirurl.txt查看")
        print("-------------------------------------")



