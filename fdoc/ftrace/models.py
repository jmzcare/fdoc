from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin
# Create your models here.


class Booker(models.Model):
    booker_name = models.CharField(max_length=30,unique=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self):
        return self.booker_name
    


class Customer(models.Model):
    customer_name = models.CharField(max_length=30,unique=True)
    customer_nature = models.ForeignKey(
        'Customer_nature', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.customer_name


class Customer_nature(models.Model):
    customer_nature_name = models.CharField(max_length=30)

    def __str__(self):
        return self.customer_nature_name


class Source_sector(models.Model):
    source_sector_name = models.CharField(max_length=30)
    customer_nature = models.ForeignKey(
        'Customer_nature', on_delete=models.CASCADE, blank=True, null=True)
    source_sector_index = models.IntegerField(default=0)
    def __str__(self):
        return self.source_sector_name


class Cargo(models.Model):
    cargo_name = models.CharField(max_length=30)

    def __str__(self):
        return self.cargo_name


class Source(models.Model):
    source_name = models.CharField(max_length=30)
    sort_index = models.IntegerField(default=0)
    source_sector = models.ForeignKey(
        'Source_sector', on_delete=models.CASCADE, null=True, blank=True)
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE, null=True, blank=True)
    customers = models.ManyToManyField(
        Customer,
        through='Sourceship',
        through_fields=('source', 'customer'),
        )
    def __str__(self):
        return self.source_name

class Sourceship(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    def __str__(self):
        return "source:{0}{1}".format(self.source.source_name,self.customer.customer_name)
    # inviter = models.ForeignKey(
    #     Person,
    #     on_delete=models.CASCADE,
    #     related_name="membership_invites",
    # )
    # invite_reason = models.CharField(max_length=64)

class Contact(models.Model):
    contact_name = models.CharField(max_length=30)
    sourceship = models.ForeignKey('Sourceship', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length = 254,blank=True)
    phone = models.CharField(max_length = 20,blank=True)
    note =  models.CharField(max_length=1000,default="")
    def __str__(self):
        return self.contact_name
    
    
class Quata(models.Model):
    quota_num = models.FloatField()
    sourceship = models.ForeignKey(
        'Sourceship', on_delete=models.CASCADE, blank=True, null=True)
    quota_date = models.DateField()
    quota_finish = models.FloatField()

    def __str__(self):
        return "source:{0}{1}|{2}:quota:{3}|finished:{4}".format(self.sourceship.source.source_name,self.sourceship.customer.customer_name, self.quota_date, self.quota_num, self.quota_finish)
