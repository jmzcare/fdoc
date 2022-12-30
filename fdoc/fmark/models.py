from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin
from mdeditor.fields import MDTextField
# Create your models here.


class Fmark(models.Model):
    subject = models.CharField(max_length=30,unique=True)
    body = MDTextField()

    def __str__(self):
        return self.subject

class FmarkSon(models.Model):
    fmark = models.ForeignKey('Fmark', on_delete=models.CASCADE)

    def __str__(self):
        return self.fmark.subject+"SON"