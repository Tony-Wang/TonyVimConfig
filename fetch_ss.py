#!/usr/bin/env python
__author__ = 'tony'
import requests
import BeautifulSoup
import sh
json_mask='''
{
	"server":"%s",
	"server_port":"%s",
	"local_port":"1080",
	"password":"%s",
	"method":"%s"
}
'''

def main():
    r = requests.post("https://www.ss-link.com/login",params={'email':'mgphuang@163.com','password':'96e79218965eb72c92a549dd5a330112','redirect':'/my/free'})
    if r.status_code != 200:
        return

    soup = BeautifulSoup.BeautifulSoup(r.content)
    trList = soup.find('tbody').findAll('tr')
    proxylist = []
    for tr in trList:
        td = tr.findAll("td")
        proxylist.append(json_mask % (td[1].text,td[2].text,td[3].text,td[4].text))
        break
    r.close()

    proxyfile = open("./proxy.json",'wt')
    proxyfile.write(proxylist[0])
    proxyfile.flush()
    proxyfile.close()

    sh.sslocal('-d','stop','-s','localhost')
    sh.sslocal('-c','proxy.json','-d','start','-s','localhost')




if __name__ == '__main__':
    main()
