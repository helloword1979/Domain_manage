# -*-coding:utf-8-*-
import os
import re
import queue
import threading
import requests
import sys

class delrep_domain:

    def __init__(self):
        self.que = queue.Queue()
        self.filename = os.path.basename(__file__)
        self.buff = ['.DS_Store',self.filename,'.git','deldobule_domains.txt','lib','img']
        self.repeat_num = 0
        self.domains = []

    #去重复
    def delRep(self):
        q = self.que
        file_dir = os.listdir()
        files = []
        domains = []

        for ln in file_dir:
            if ln in self.buff:
                continue
            files.append(ln)
        print("[+] subdomain file lists:",end="")
        print(files)

        for file in files:
            lines = open(file,"r")
            for line in lines:
                line = line.rstrip()
                q.put(line)
        
        while not q.empty():
            rubbish = q.get()
            r = re.search(r"[a-zA-Z0-9\*][-a-zA-Z0-9]{0,62}(.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+.?",rubbish)
            if r:
                domain = r.group().split(" ")[0].split(",")[0]
            if domain in domains:
                self.repeat_num+=1
                continue
            if '@' in domain:
                continue

            domains.append(domain)

        self.domains=domains
        return self._writeFile()

    #保存
    def _writeFile(self):
        domains = self.domains
        
        if os.path.exists('deldobule_domains.txt'):
        	os.remove('deldobule_domains.txt')
        for i in domains:
            with open("deldobule_domains.txt","a+") as f:
                f.write(i+"\n")
        print("[+] repeat repeat_num of subdomain：{}".format(self.repeat_num))
        print("[+] The subdomains is storage in deldobule_domains.txt")

    #子域名探测
    def Subdomain_explore(self,q):
        while not q.empty():
            domain = q.get()
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
                'Connection': 'close'
            }
            try:
                requests.adapters.DEFAULT_RETRIES = 5
                request = requests.get(url='http://'+domain,headers=headers,timeout=4)
                if request.encoding == 'ISO-8859-1':
                    encodings = requests.utils.get_encodings_from_content(request.text)
                    request.encoding = encodings[0]
                else:
                    request.encoding = 'utf-8'
                Status = request.status_code
                if '<title>' in request.text:
                    title = 'title：'+re.findall(r'<title>(.*?)</title>',request.text)[0]
                else:
                    title= None

                if request.headers.get('Server'):
                    Server = request.headers.get('Server')
                else:
                    Server = None
                table = '|%-21s|%-6s|%-20s|%-30s' % (domain, Status, Server, title)
                print(table)
            except:
                try:
                    request = requests.get(url='https://'+domain,headers=headers,timeout=4)
                    if request.encoding == 'ISO-8859-1':
                        encodings = requests.utils.get_encodings_from_content(request.text)
                        request.encoding = encodings[0]
                    else:
                        request.encoding = 'utf-8'
                    Status = request.status_code
                    if '<title>' in request.text:
                        title = 'title：'+re.findall(r'<title>(.*?)</title>',request.text)[0]
                    else:
                        title= None

                    if request.headers.get('Server'):
                        Server = request.headers.get('Server')
                    else:
                        Server = None
                    table = '|%-21s|%-6s|%-20s|%-30s' % (domain, Status, Server, title)
                except:
                    Status = None
                    title= None
                    Server = None
                    table = '|%-21s|%-6s|%-20s|%-30s' % (domain, Status, Server, title)
                    print(table)


    def get_domains(self,threads):
        domains=[]
        lines = open('deldobule_domains.txt',"r")
        for line in lines:
            line = line.rstrip()
            domains.append(line)   

        q = self.que

        for domain in domains:
            q.put(domain)

        for num in range(threads):
                t = threading.Thread(target=self.Subdomain_explore,args=(q,))
                t.start()

if __name__ == "__main__":
    Domain = delrep_domain()
    if sys.argv[1] == 'delrep':
        deldb_domains=Domain.delRep()
    elif sys.argv[1] == 'scan':
        Domain.get_domains(50)
    else:
        print("please input python domain_manage.py delrep|scan")


