from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Blog, Tag
from website.settings import logger
def index(request):
    logger.info(request.GET)
    logger.info(request.GET.get('tag'))
    data = {
        'tags' : Tag.objects.all(),
        'blogs' : Blog.get_all(request.GET.get('tag')),
    }
    return render(request, 'qtblog/index.html', data)
def blog(request):
    path = request.path#re.match('.*/([^/]*)$', request.path).group(1)
    if path == '':
        return HttpResponseRedirect('/')
    blog = Blog.get_blog_path(path)
    if request.method == 'POST':
        (ret, message) = Blog.try_save(request.POST, path, request.user, blog)
        return HttpResponse(message)
    
    if blog is None:
        if (not Blog.create_check(request.user)):
            return HttpResponse('blog not exist')
        if 'edit' in request.GET:
            return edit_blog(request, blog)
        return HttpResponseRedirect(path + '?edit=');
    else :
        if 'edit' in request.GET:
            return edit_blog(request, blog)
        return show_blog(request, blog)

def edit_blog(request, blog):
    context = {'blog':blog}
    return render(request, 'qtblog/blog_edit.html', context)

def show_blog(request, blog):
    if (not blog.read_check(request.user)):
        return HttpResponse('blog not exist')
    context = {'blog': blog}
    return render(request, 'qtblog/blog.html', context)

# Create your views here.
