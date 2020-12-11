from __future__ import unicode_literals
from django.db import models

# Create your models here.

class ContactForm(models.Model):
    
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    txt = models.TextField()
    name = models.CharField(max_length=50)
    date = models.CharField(max_length=20, default="")
    time = models.CharField(max_length=20, default="")


    def __str__(self):
        return self.name