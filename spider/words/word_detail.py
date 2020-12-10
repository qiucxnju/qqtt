#!/usr/bin/python3

import urllib
import urllib.request
import time
import json
import hashlib
import os
import spider
from bs4 import BeautifulSoup

tasks = [
    {'ename': '固不可彻', 'jumplink': 'https://hanyu.baidu.com/zici/s?wd=%E5%9D%9A%E4%B8%8D%E5%8F%AF%E6%91%A7&cf=synant&ptype=zici'}
];
def read_data(html):
    soup = BeautifulSoup(html, features='html.parser')
    name = soup.find(id="pinyin").find("strong").text.strip()
    pinyin = soup.find(id="pinyin").find("b").text.strip()
    try:
        mean = soup.find(id="basicmean").find_parents(class_="content")[0].find("dd").text.strip()
    except:
        mean = None
    try:
        detail = soup.find(id="detailmean").find_parents(class_="content")[0].find(class_="tab-content").text.strip()
    except:
        detail = None
    try:
        source = soup.find(id="source-wrapper").find(class_="tab-content").text.strip()
    except:
        source = None
    syn = []
    try:
        for s in soup.find(id="synonym").find(class_="block").find_all("a"):
            syn += [s.text.strip()]
    except:
        1
    ant = []
    try:
        for s in soup.find(id="antonym").find(class_="block").find_all("a"):
            ant += [s.text.strip()]
    except:
        1
    try:
        baike = soup.find(id="baike-wrapper").find(class_="tab-content").text[:-8].strip()
    except:
        baike = None
    return {
        'name' : name,
        'pinyin' : pinyin,
        'mean' : mean,
        'detail' : detail,
        'source' : source,
        'syn' : syn,
        'ant' : ant,
        'baike' : baike,
    }

def get_detail(html, context):
    try:
        soup = BeautifulSoup(html, features='html.parser')
        name = soup.find(id="pinyin").find("strong").string;
        if (name == context['ename']):
            return str(soup)
        return None
    except :
        return None
f = open("word_list.txt", "r");
data = "\n".join(f.readlines())
f.close()
tasks = json.loads(data);
k = 0
total_data = []
for i in tasks:
    a = 100
    k += 1
    #if (k < 250): continue;
    #if (k > 2): break
    print(k)
    print(i)
    url = i['jumplink']
    data = None
    while (data is None):
        data = spider.cache_get("./word_detail/", url, get_detail, i)
        if (data):
            break;
        print("retry:", a)
        time.sleep(a)
        a *= 10
    total_data += [read_data(data)]
print(total_data)
f = open("word_detail.txt", "w");
f.write(json.dumps(total_data, indent = 4));
f.close()


    

