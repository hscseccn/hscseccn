'''
Function:
    基于TCP的端口扫描
Author:
    spmonkey
邮箱：
    spmonkey@hscsec.cn
'''
# -*- coding: utf-8 -*-
from socket import *
import queue
import threading
import re
import time


class portscan:
    def __init__(self, ips=None, thread=None):
        self.ips = ips
        self.thread = thread
        self.threads = []
        self.q = queue.Queue()
        self.stop = 0
        self.lock = threading.RLock()

    def port(self):
        for port in range(1, 65536):
            self.q.put(port)

    '''socket'''
    def port_scan(self, ip):
        # with self.lock:
        while True:
            # self.lock.acquire()
            port = self.q.get()
            # time.sleep(1)
            # print(f"\r{ip}:{port}", end="")
            # time.sleep(1)
            try:
                s = socket(AF_INET, SOCK_STREAM)        # 会断网
                s.connect((ip, port))
                s.shutdown(1)
                # print(f"{ip}:{port}")
                if port == 3306:
                    print(f"\r[+] {ip}:{port} is open => Service is mysql")
                elif port == 1521:
                    print(f"\r[+] {ip}:{port} is open => Service is oraclesql")
                elif port == 5000:
                    print(f"\r[+] {ip}:{port} is open => Service is DB2")
                elif port == 5432:
                    print(f"\r[+] {ip}:{port} is open => Service is PostgreSQL")
                elif port == 5236:
                    print(f"\r[+] {ip}:{port} is open => Service is DM")
                elif port == 6379:
                    print(f"\r[+] {ip}:{port} is open => Service is Redis")
                else:
                    try:
                        services = getservbyport(port)
                        print(f"\r[+] {ip}:{port} is open => Service is {services}")
                    except:
                        print(f"\r[+] {ip}:{port} is open => Service is undefined")
            except Exception as e:
                # print(e)
                pass
            # finally:
            #     self.lock.release()
            if self.q.qsize() == 0:
                time.sleep(0.5)
                self.stop += 1
                break



    def main(self):
        setdefaulttimeout(0.5)
        self.port()
        print(f"当前启用的线程数：{self.thread}")
        print()
        if '0/24' in self.ips:
            ip_re = re.compile('(.*)\.0/24')
            ip_c = ip_re.findall(self.ips)[0]
            for ip in range(255):
                a = f'{ip_c}.{ip}'
                for i in range(self.thread):
                    t = threading.Thread(target=self.port_scan, args=(a,))
                    t.daemon = 1
                    self.threads.append(t)
                for j in self.threads:
                    j.start()
                while 1:
                    if self.stop >= 1:
                        break
        elif '1/24' in self.ips:
            ip_re = re.compile('(.*)\.1/24')
            ip_c = ip_re.findall(self.ips)[0]
            for ip in range(1, 256):
                a = f'{ip_c}.{ip}'
                for i in range(self.thread):
                    t = threading.Thread(target=self.port_scan, args=(a,))
                    t.daemon = 1
                    self.threads.append(t)
                for j in self.threads:
                    j.start()
                while 1:
                    if self.stop >= 1:
                        break
        else:
            for i in range(self.thread):
                t = threading.Thread(target=self.port_scan, args=(self.ips,))
                t.daemon = 1
                # t.start()
                self.threads.append(t)
            for j in self.threads:
                j.start()
            while 1:
                if self.stop >= 1:
                    break
            print("\r")

