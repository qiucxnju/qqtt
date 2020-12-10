#!/usr/bin/python3

import urllib
import urllib.request
import time
import json
import hashlib
import os
base_url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28204&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=%E6%88%90%E8%AF%AD&sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&"
MAX_P = 1447
EACH_W = 30
begin = 0


TIME = 1
def cache_get(d, url, get_data):
    file_name = d + hashlib.sha224(url.encode("utf-8")).hexdigest()
    if (os.path.isfile(file_name)):
        fil = open(file_name, 'r')
        data = "\n".join(fil.readlines())
        fil.close()
        return data
    time.sleep(TIME)
    response = urllib.request.urlopen(url)
    html = response.read()
    data = get_data(html)
    if data:
        fil = open(file_name, 'w')
        fil.write(data)
        fil.close()
    return data
def get_list(html):
    try:
        data = json.loads(html)['data'][0]['result']
        print(data)
        return json.dumps(data)
    except :
        return None
total_data = []
for i in range(0, MAX_P):
    url = base_url + '&pn=' + str(begin) + '&rn=30'
    print(i, begin, url);
    a = 100
    data = None
    while (data is None):
        data = cache_get("./word_list/", url, get_list)
        if data:
            break
        print("retry:", a)
        time.sleep(a)
        a *= 10
    begin += 30
    total_data += json.loads(data)
f = open("word_list.txt", "w");
f.write(json.dumps(total_data, indent = 4));
f.close()
