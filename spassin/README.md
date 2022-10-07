# spassin扫描工具使用说明
> 使用方法

python spassin.py -h
![HELP](./picture/help.png)
注：1、本程序默认线程数为 10，线程数可调，参数为：-T/--thread
   2、本程序支持设置代理，不过仅限 webscan、domain参数

> cdn查询

* python spassin.py --cdn -u www.baidu.com
![CDN](./picture/cdn1.png)
* python spassin.py --cdn --url www.baidu.com
![CDN](./picture/cdn2.png)

> 端口扫描

* python spassin.py --port -i 192.168.111.128 -T 65535
![PORT](./picture/port1.png)
* python spassin.py --port --ip 192.168.111.128 --thread 65535
![PORT](./picture/port2.png)

> web资产收集

* python spassin.py --webscan -u www.hscsec.cn -T 50
![WEBSCAN](./picture/webscan1.png)
* python spassin.py --webscan --url www.hscsec.cn --thread 50 --proxy 127.0.0.1:10809
![WEBSCAN](./picture/webscan2.png)
**注：webscan可以通过 proxy参数 进行本地全局代理的配置**

> 子域名查询

* python spassin.py --domain -u hscsec.cn -T 50 --proxy 127.0.0.1:10809 
![DOMAIN](./picture/domain1.png)
* python spassin.py --domain --url hscsec.cn --thread 50 --proxy 127.0.0.1:10809
![DOMAIN](./picture/domain2.png)

