#!-*-coding:utf-8 -*-
from django.db import models
import hashlib, datetime, os
from datetime import datetime
import re
from website import settings
from django.contrib.auth.models import User
from website.settings import logger



class File(models.Model):
    title = models.CharField(max_length = 20) 
    path = models.CharField(max_length = 100) 
    src = models.CharField(max_length = 100) 
    owner = models.ForeignKey(User,on_delete=models.CASCADE,) 
    date = models.DateTimeField()

    @staticmethod
    def create_check(user):
        if (not user.is_staff):
            return False
        return True

    @staticmethod
    def show_file_path(path):
        logger.info(path)
        files = File.objects.filter(path = path)
        logger.info(files)


        if len(files) > 0: 
            fil = files[0]
        else:  
            return None

        return fil


    @staticmethod
    def get_all():
        files = File.objects.all().order_by('-date')
        return files

    @staticmethod 
    def createPath(fil):
        exist = True
        name = ""
        folder = datetime.now().strftime('%Y%m%d')
        p = './' + settings.FILE_SRC + folder
        if not os.path.exists(p):
            os.makedirs(p)
        m = re.search(r'(\.[^.]+)$', fil.name)
        while exist:    
            s = ("%s%s" % (name.encode("utf-8"), str(datetime.now()))).encode("utf-8");
            name = folder + '/' + hashlib.sha224(s).hexdigest()
            if m is not None:
                name += m.group(1)
            path = "%s%s" % (settings.FILE_PATH, name)
            src = "%s%s" % (settings.FILE_SRC, name)
            exist = os.path.isfile(src) 
        return (name, path, src)

    @staticmethod
    def try_save(data, fil, user):

        (name, path, src) = File.createPath(fil)
        logger.info(path)
        dest = open('./' + src, 'wb')
        for chunk in fil.chunks():
            dest.write(chunk)
        dest.close()
        fil = File(title = "%s_%s" % (data['title'], re.search(r'^([^.]+)', fil.name).group(0)) ,
            path = path,
            src = src,
            owner = user,
            date = datetime.now(),
            )
        fil.save() 
        return fil
# Create your models here.
