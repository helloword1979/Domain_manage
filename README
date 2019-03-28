
### Domain_manage
自动化子域名简单收集+去重+获取网站banner信息。

-m参数 暂时只有两个模块

#### delrep
只有-u参数会默认执行delrep模块

首先会从crt.sh上爬取该域名SSL证书中的子域名，写入crt_ssl_domains.txt。
然后会扫描目录下所有文件中的子域名，除去deldobule_domains.txt、lib、.git、.DS_Store、README.md、img以及domain_manage.py。
然后去重并写入deldobule_domains.txt。

#### scan
爬取deldobule_domains.txt中子域名的banner信息。

#### help
```
[+] example: python domain_manage.py -u baidu.com -m delrep -t 50

-h,--help : 				show this help message and exit

-u TARGET,--url=TARGET : 	Domain names to be scanned

-t , --threads=numbers :			Number of threads crawling banner information from websites

-m , --moudle=delrep :				Execution module [delrep|scan]
```

#### DEMO
![demo](https://github.com/Smi1e521/Domain_manage/img/demo.jpg)

