from django.db import models
from datetime import datetime

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pages = models.IntegerField()
    publisher =  models.CharField(max_length=200)
    category =  models.CharField(max_length=200)
    avaiable_date =  models.DateField(auto_now=True) #keep track of when the book will be available

    @property
    def is_avaliable(self):
        if  self.avaiable_date > datetime.date.today():
            return False
        return True


class Customers(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email =  models.EmailField(max_length=200)

class BookHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    date_borrowed =  models.DateField(auto_now=True)
    date_returned =  models.DateField(null=True, blank=True)

    @property
    def is_avaliable(self):
        if  self.date_returned > datetime.date.today():
            return False
        return True