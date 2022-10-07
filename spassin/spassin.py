'''
Function:
    spscan
Author:
    spmonkey
邮箱：
    spmonkey@hscsec.cn
'''
# -*- coding: utf-8 -*-
from function.portscan import portscan
from function.cdnscan import CDN
from function.son_domain import domain
from function.webscan import webscan
from function.dirb import directory
import sys
import argparse


def argument():
    parser = argparse.ArgumentParser()
    try:
        parser.add_argument('--port', action='store_true', help="端口扫描")
        parser.add_argument('--cdn', action='store_true', help="cdn查询")
        parser.add_argument('--dirb', action='store_true', help="目录扫描")
        parser.add_argument('--webscan', action='store_true', help="web资产收集")
        parser.add_argument('--domain', action='store_true', help="子域名查询")
        parser.add_argument('--proxy', type=str, default=None, help="代理设置，例：--proxy 127.0.0.1:10809")
        parser.add_argument('-T', '--thread', type=int, default=10, help="线程设置，例：--thread 10，本工具默认使用 10线程")
        parser.add_argument('--xc', type=str, default=None, help="字典路径参数，例：--xc /usr/share/wordlists/dirb/common.txt，注：CMS查询的字典需为json格式")
        parser.add_argument('-u', '--url', type=str, default=None, help="url，例：--url http://www.baidu.com/")
        parser.add_argument('-i', '--ip', type=str, default=None, help="ip，例：--ip 127.0.0.1")
        # parser.add_argument('-d', '--domain', type=str, default=None, help="子域名查询，例：--domain baidu.com")
        args = parser.parse_args()
        return args
    except Exception as e:
        pass

class main:

    # cdn查询
    def cdn_main(self, url):
        print('''
           .___                                  
  ____   __| _/____   ______ ____ _____    ____  
_/ ___\ / __ |/    \ /  ___// ___\\\\__  \  /    \ 
\  \___/ /_/ |   |  \\\\___ \\\\  \___ / __ \|   |  \\
 \___  >____ |___|  /____  >\___  >____  /___|  /
     \/     \/    \/     \/     \/     \/     \/ 
                    ''')
        print(f'''
目标IP：{url}
            ''')
        print("-------------开始cdn查询--------------")
        cdn = CDN(url)
        return cdn.CDNScan()

    # 端口扫描
    def port_main(self, ip, thread):
        print('''
                      __                               
______   ____________/  |_  ______ ____ _____    ____  
\____ \ /  _ \_  __ \   __\/  ___// ___\\\\__  \  /    \ 
|  |_> >  <_> )  | \/|  |  \___ \\\\  \___ / __ \|   |  \\
|   __/ \____/|__|   |__| /____  >\___  >____  /___|  /
|__|                           \/     \/     \/     \/ 
            ''')
        print(f'''
目标IP：{ip}
            ''')
        print("-------------开始端口扫描--------------")
        port = portscan(ips=ip, thread=thread)
        ip_list = port.main()
        for data in ip_list:
            print(data)
        print("")

    # 子域名查询
    def domain_main(self, url, thread, proxy):
        print("""
    .___                    .__        
  __| _/____   _____ _____  |__| ____  
 / __ |/  _ \ /     \\\\__  \ |  |/    \\
/ /_/ (  <_> )  Y Y  \/ __ \|  |   |  \\
\____ |\____/|__|_|  (____  /__|___|  /
     \/            \/     \/        \/ 
            """)
        print(f'''
目标IP：{url}
            ''')
        print("------------开始子域名查询-------------")
        son = domain(domain=url, proxies=proxy, thread=thread)
        son.main()

    # web资产收集
    def webscan_main(self, url, thread, proxy, file_name):
        print('''
              ___.                                
__  _  __ ____\_ |__   ______ ____ _____    ____  
\ \/ \/ // __ \| __ \ /  ___// ___\\\\__  \  /    \ 
 \     /\  ___/| \_\ \\\\___ \\\\  \___ / __ \|   |  \\
  \/\_/  \___  >___  /____  >\___  >____  /___|  /
             \/    \/     \/     \/     \/     \/ 
            ''')
        print(f'''
目标IP：{url}
            ''')
        print("------------开始指纹识别查询-------------")
        web = webscan(url=url, proxies=proxy, thread=thread, file_name=file_name)
        web.webscan()

    # 目录查询
    def dirb_main(self, url, thread, proxy, file_name):
        print("""
    .___.__      ___.    
  __| _/|__|_____\_ |__  
 / __ | |  \_  __ \ __ \\ 
/ /_/ | |  ||  | \/ \_\ \\
\____ | |__||__|  |___  /
     \/               \/ 
        """)
        print(f'''
目标IP：{url}
                ''')
        print("------------开始目录扫描-------------")
        dirbscan = directory(url=url,thread=thread, proxies=proxy, file_name=file_name)
        dirbscan.main()


if __name__ == "__main__":
    args = argument()
    spassin = main()
    try:
        if args.dirb:
            spassin.dirb_main(url=args.url, thread=args.thread, proxy=args.proxy, file_name=args.xc)
        elif args.port:
            spassin.port_main(ip=args.ip,thread=args.thread)
        elif args.cdn:
            print(spassin.cdn_main(url=args.url))
        elif args.domain:
            spassin.domain_main(url=args.url, thread=args.thread, proxy=args.proxy)
        elif args.webscan:
            spassin.webscan_main(url=args.url, thread=args.thread, proxy=args.proxy, file_name=args.xc)
    except Exception as e:
        pass