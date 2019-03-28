from lib import domain_manage
from lib import ssl_domain
import sys
import os
import getopt

def help():
	print(
		"""
[+] example: python domain_manage.py -u baidu.com -m delrep -t 50

-h,--help : 		 show this help message and exit

-u TARGET,--url=TARGET : Domain names to be scanned

-t , --threads=numbers : Number of threads crawling banner information from websites

-m , --moudle=delrep :	 Execution module [delrep|scan]
		""")


def main():
	domains = ""
	module = "delrep"

	if len(sys.argv) == 1:
		help()
		sys.exit()

	try:
		opts,args = getopt.getopt(sys.argv[1:], "hutm:",["help","url=","threads=","moudle="])

	except:
		print("argv error,please input")


	for option,value in opts:
		if option in ["-h","--help"]:
			help()
			sys.exit()

		elif option in ["-u","--url"]:
			domains = value

		elif option in ["-t","--threads"]:
			threads = value

		elif option in ["-m","--moudle"]:
			module = value

	manage = domain_manage.delrep_domain()
	if module == 'delrep':
		#通过SSL获取子域名
		ssl = ssl_domain.ssl_domain(domains)
		ssl.get_domain()

		#去重
		manage.delRep()

	elif module == 'scan':
		#获取网站banner
		manage.get_domains(threads=50)
	else:
		help()

if __name__ == '__main__':
	main()