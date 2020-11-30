from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Location(models.Model):
    people = models.ForeignKey(User)
    date = models.DateTimeField(True)
    longitude = models.
    
