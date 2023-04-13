from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20, null=False, unique=True)
    password = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True)
    money = models.IntegerField(max_length=50, null=False)



