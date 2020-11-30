from django.db import models
import logging
from datetime import datetime, date, time
import json
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)
BLOG_STATE_VALID = 0
BLOG_STATE_INVALID = 1

class Tag(models.Model):
    value = models.CharField(max_length = 20)

class Blog(models.Model):
    # for all the documentations!!
    title = models.CharField(max_length = 20) # article title
    date = models.DateField()
    modify = models.DateField()
    path = models.CharField(max_length = 100) # article path
    content = models.TextField() # the wiki body
    owner = models.ForeignKey(User,on_delete=models.CASCADE,) # owner id
    state = models.IntegerField()
    tags = models.ManyToManyField(Tag)


    

    @staticmethod
    def get_all(tag = None):
        if (tag is None):
            blogs = Blog.objects.filter(state = BLOG_STATE_VALID).order_by('-date')
        else:
            tag = Tag.objects.filter(value=tag)
            logger.info(tag);
            blogs = Blog.objects.filter(tags__in= tag, state = BLOG_STATE_VALID).order_by('-date')
        return blogs

    @staticmethod
    def get_blog_path(path):
        blogs = Blog.objects.filter(path = path, state = BLOG_STATE_VALID)
        if len(blogs) > 0: blog = blogs[0]
        else: blog = None
        return blog
    
    def read_check(blog, user):
        return True

    @staticmethod
    def create_check(user):
        if not user.is_stuff: 
            return False
        return True
    
    @staticmethod
    def try_save(data, path, user, blog):
        logging.info(data)

        if not Blog.create_check(user):
            return (False, "please login first")
        
        new_blog = Blog(
            title = data['title'],
            date = datetime.strptime (data['date'], '%Y-%m-%d'),
            modify = datetime.now(),
            path = path,
            content = data['content'],
            owner = user,
            state = BLOG_STATE_VALID,
            )
        tag_list = []
        for value in json.loads(data['tags']):
            tags = Tag.objects.filter(value = value)
            if len(tags) == 0:
                tag = Tag(value = value)
                tag.save()
            else: 
                tag = tags[0]
            tag_list.append(tag)
        new_blog.save()
        for tag in tag_list:
            new_blog.tags.add(tag)
        if blog is not None:
            blog.state = BLOG_STATE_INVALID
            blog.save()
        return (True, "success")

# Create your models here.
