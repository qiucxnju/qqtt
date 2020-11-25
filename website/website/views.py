from django.shortcuts import render
from django.http import HttpResponse
import yaml
import logging

from website import settings 

import traceback
import smtplib
from email.utils import formataddr
import email.mime.text 

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
def sendMail(request):
    logging.info(request.POST['content'])
    try:
        smtp = smtplib.SMTP_SSL(settings.SITE['stmp_addr'])  
        smtp.login(settings.SITE['email_send'],settings.SITE['email_pwd'])  
        msg = email.mime.text.MIMEText(request.POST['content'], _charset='utf-8')
        msg['From'] = settings.SITE['email_send']  
        msg['To'] = settings.SITE['email']
        msg['Subject']=settings.SITE['email_subject']
        smtp.sendmail(settings.SITE['email_send'],settings.SITE['email'],msg.as_string())  
        smtp.quit()  
        return HttpResponse('发送成功')
    except Exception as e:
        exstr = traceback.format_exc()
        logging.error(exstr)
        smtp.quit()
        return HttpResponse("发送失败")

def error(request):
    return index(request)
