#-*- coding:utf-8 -*-
#version = 0.1.1  可以获得无序的代理列表
#version = 0.1.2  可写入csv文件
#version = 0.1.3  可获取无空行的csv文件
#version = 0.1.4  可获取高匿HTTPS和HTTP列表

from bs4 import BeautifulSoup
import os
import re
import csv
import time
import random
import chardet
import requests
import crack
import pandas as pd

class GetInfo(object):
    def __init__(self):
        self.url = 'http://www.xicidaili.com/'

    def get_random_headers(self):
        return random.choice(crack.agents)

    def get_random_proxies(self):
        return random.choice(crack.proxies)

    def get_response_text(self,url):
        headers = {'User-Agent':self.get_random_headers()}
        proxies = {'http':self.get_random_proxies()}
        r = requests.get(url,headers=headers,proxies=proxies)
        r.encoding = chardet.detect(r.content)['encoding']
        return r.text

    def spider(self,url):
        items = []
        response_text = self.get_response_text(url)
        soup = BeautifulSoup(response_text,'lxml')
        tags_1 = soup.find_all('tr',attrs={'class':''})
        tags_2 = soup.find_all('tr',attrs={'class':'odd'})
        tags = tags_1 + tags_2
        all_list = dict.fromkeys(range(len(tags)), None)
        for i in range(0,len(tags)):
            one_list = []
            for string in tags[i].stripped_strings:
                one_list.append(repr(string))
            for index,string in enumerate(one_list):
                one_list[index] = eval(string)
            all_list[i] = one_list
        for i in all_list:
            all_list[i] = ','.join(all_list[i])

        file_name = 'proxy.txt'
        pattern = re.compile(r'^\d')
        with open(file_name,'w') as fp:
            for i in all_list:
                if len(pattern.findall(all_list[i])):
                    fp.write(all_list[i] + '\n')

        with open('proxy.csv', 'wt') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            # 读要转换的txt文件，文件每行各词间以,字符分隔
            with open('proxy.txt', 'rt') as filein:
                for line in filein:
                    line_list = line.strip('\n').split(',')
                    spamwriter.writerow(line_list)

        with open('proxy.csv','rt')as fin:  #读有空行的csv文件，舍弃空行
            lines=''
            for line in fin:
                if line!='\n':
                    lines+=line

        with open('proxy.csv','wt')as fout:  #再次文本方式写入，不含空行
            fout.write(lines)

getinfo = GetInfo()
getinfo.spider('http://www.xicidaili.com/')

################################################################################
filepath = 'C:\\Users\\Clarence\\Documents\\Code\\Python\\Getproxy\\proxy.csv'
proxy_csv = pd.read_csv(filepath,header=None,encoding='ansi')
proxy_csv.columns = list('abcdefg')
https = proxy_csv.loc[:,['a','b']]\
                     [(proxy_csv['e']=='HTTPS')&(proxy_csv['d']=='高匿')]
http = proxy_csv.loc[:,['a','b']]\
                    [(proxy_csv['e']=='HTTP')&(proxy_csv['d']=='高匿')]
https.to_csv('https.csv',sep=':',header=False,index=False)
http.to_csv('http.csv',sep=':',header=False,index=False)

with open('http.csv', 'rt') as filein:
    lines = []
    for line in filein:
        line = line.strip('\n')
        line = '\'http://'+line+'\''+','+'\n'
        lines.append(line)
with open('http.txt','wt') as fileout:
    for line in lines:
        fileout.write(line)

with open('https.csv', 'rt') as filesin:
    lines = []
    for line in filesin:
        line = line.strip('\n')
        line = '\'https://'+line+'\''+','+'\n'
        lines.append(line)
with open('https.txt','wt') as filesout:
    for line in lines:
        filesout.write(line)

os.remove('proxy.txt')
os.remove('proxy.csv')
os.remove('http.csv')
os.remove('https.csv')
