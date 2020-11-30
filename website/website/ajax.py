from django.http import HttpResponse
import traceback
import smtplib
from email.utils import formataddr
import email.mime.text 
from website import settings
from website.settings import logger
from qtblog.templatetags.blog_filter import mark_down
from qtblog.models import Tag
import json

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

def markDown(request):
    return HttpResponse(mark_down(request.POST['content']))

def loadTags(request):
    tags = json.loads(request.GET['tags'])
    logger.info(tags)
    
    ret_tags = []
    for tag in Tag.objects.all():
        value = tag.value
        if value not in tags:
            ret_tags.append(value)
    return HttpResponse(json.dumps(ret_tags))

