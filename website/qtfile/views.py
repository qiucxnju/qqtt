from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from qtfile.models import File
from website.settings import logger
import os

def upload(request):
    if (not File.create_check(request.user)):
        return HttpResponse("你没有权限")
    if request.method == 'POST':
        rsp = 'Your file path is'
        for afile in request.FILES.getlist('files'):
            fil = File.try_save(request.POST, afile, request.user)
            rsp += '<br><a href="%s"> > ![%s](%s)</a><br>' % (fil.path, fil.title, fil.path)
        rsp += '<br>It can be directly pasted in a wiki link.';
        return HttpResponse(rsp)
    return render(request, 'qtfile/upload.html', {'title': request.GET.get('title', None)})

def list(request):
    data = {
        'files' : File.get_all()
    }
    return render(request, 'qtfile/index.html', data)

def download(request):
    logger.info(request)
    
    path = request.path
    fil = File.show_file_path(path)
    if (fil is None) :
        return HttpResponse('file not exist')
    response = HttpResponse()
    response['Content-Length'] = os.path.getsize('./' + fil.src)
    response['X-Accel-Redirect'] = fil.src
    logger.info(os.path.getsize('./' + fil.src))
    logger.info(fil.src)
    logger.info(response);
    return response

# Create your views here.
