from django.shortcuts import render
from django.http import HttpResponse
from website.settings import logger
def index(request):
    return render(request, 'qttool/index.html')
def words(request):
    word = request.GET.get("word", "");
    logger.info(word)
    q = word[-1:]
    logger.info(q)
    f = open("static/data/words.txt", "r")
    w = f.readlines()
    w = filter(lambda x : x.startswith(q), w)
    f.close();
    return render(request, 'qttool/words.html', {'word': word, 'words':w})
# Create your views here.
