#!/usr/bin/python3

import urllib
import urllib.request
import time
import json
import hashlib
import os

TIME = 1
def cache_get(d, url, get_data, context):
    file_name = d + hashlib.sha224(url.encode("utf-8")).hexdigest()
    if (os.path.isfile(file_name)):
        fil = open(file_name, 'r')
        data = "\n".join(fil.readlines())
        fil.close()
        return data
    time.sleep(TIME)
    response = urllib.request.urlopen(url)
    html = response.read()
    data = get_data(html, context)
    if data:
        fil = open(file_name, 'w')
        fil.write(data)
        fil.close()
    return data

