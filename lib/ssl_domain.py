import requests
import re
import os

class ssl_domain:

	def __init__(self,domain):
		self.domain = domain
		self.url = 'https://crt.sh/?q=%.'
		self.headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
                'Connection': 'close'
            }
		self.ssl_domains = []

	def get_html(self,url):
		headers = self.headers
		requests.packages.urllib3.disable_warnings()
		while 1:
			try:
				r = requests.get(url,headers=headers,timeout=10,verify=False)
				r.raise_for_status()
				r.encoding=r.apparent_encoding
				return r.text
			except:
				continue

	def get_domain(self):
		url = self.url + self.domain
		html = self.get_html(url)

		domains = re.findall(r'<TD>(.*?\.{})</TD>'.format(self.domain),html)
		self.ssl_domains = domains
		self.write(domains)

	def write(self,domains):
		if os.path.exists('crt_ssl_domains.txt'):
			os.remove('crt_ssl_domains.txt')

		print("ssl domian:")
		for i in domains:
			with open("crt_ssl_domains.txt","a+") as f:
				print(i)
				f.write(i+"\n")

if __name__ == '__main__':

	ssl = ssl_domain('kuaishou.com')
	ssl.get_domain()