from django.db import models


# Create your models here.
class Symbol(models.Model):
    name = models.CharField(max_length=1024,unique = True)
    fullName = models.CharField(max_length=1024)
    feeCurrency = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
