from django.shortcuts import render
from django.http import HttpResponse
from website.settings import logger
import json
def index(request):
    return render(request, 'qttool/index.html')
def words(request):
    word = request.GET.get("word", "");
    logger.info(word)
    q = word[-1:]
    logger.info(q)
    f = open("static/data/words.txt", "r")
    w = f.readlines()
    f.close();
    words = json.loads("\n".join(w))

    info = {}
    for i in words:
        if (i['name'] == word):
            info = i
    logger.info(info)
    words = filter(lambda x : x['name'].startswith(q), words)
    
    return render(request, 'qttool/words.html', {'word': word, 'info':info, 'words':words})
# Create your views here.
