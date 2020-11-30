from django.shortcuts import render
from django.http import HttpResponse
import yaml
import logging

from website import settings 


logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    event = yaml.load(open("static/data/event.yaml", 'r'))
    logger.info(event)
    return render(request, 'website/index.html', event)
def member(request):
    member = yaml.load(open("static/data/member.yaml", 'r'))
    logger.info(member)
    return render(request, 'website/member.html', member)
def contact(request):
    return render(request, 'website/contact.html') 

