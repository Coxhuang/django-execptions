from django.db import models



class Student(models.Model):

    name = models.CharField(max_length=128,unique=True)
    age = models.CharField(max_length=128,default="1")