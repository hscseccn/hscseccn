'''
Function:
    CMS识别
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
import sys
import os
import requests
import json
import queue
import time
import threading
from requests.packages.urllib3 import disable_warnings
from hashlib import *
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from lib.get_user_agent import get_user_agent
disable_warnings()

class CMScan:
    def __init__(self, url=None, thread=None, file_name=None):
        self.url = url
        self.headers = get_user_agent()
        self.q = queue.Queue()
        self.result = []
        self.stop = 0
        self.count = 0
        self.thread = thread
        self.file_name=None

    def CMS_file(self):
        CMSprint = open(self.file_name, "r", encoding="utf-8")
        CMSprint_json = json.load(CMSprint)
        for i in range(len(CMSprint_json["RECORDS"])):
            self.q.put(CMSprint_json["RECORDS"][i])

    def CMScan(self):
        while True:
            cms = self.q.get()
            if self.q.qsize() == 0:
                self.stop += 1
                break
            elif cms["checksum"]:
                urls = self.url + cms["staticurl"]
                result = requests.get(url=urls, headers=self.headers, verify=False, timeout=5)
                cms_md5 = md5(result.content).hexdigest()
                if cms_md5 == cms["checksum"]:
                    print(f'CMS为：{cms["remark"]}')
                    self.stop += 1
            elif cms["homeurl"]:
                urls = self.url + cms["homeurl"]
                result = requests.get(url=urls, headers=self.headers, verify=False, timeout=5)
                result.encoding = "utf-8"
                if cms["keyword"] in result.text:
                    print(f'CMS为：{cms["remark"]}')
                    self.stop += 1
                    break


    def CMScan_main(self):
        self.CMS_file()
        t_list = []
        for i in range(self.thread):
            t = threading.Thread(target=self.CMScan, args=())
            t.daemon = 1
            t_list.append(t)
        for j in t_list:
            j.start()
        while True:
            time.sleep(0.5)
            if self.stop:
                time.sleep(1)
                break



