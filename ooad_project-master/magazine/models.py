from unicodedata import category
from django.db import models
# Create your models here.
class CategoriesList(models.Model):
    # id = models.AutoField(primary_key=True)
    category_name = models.TextField(primary_key=True)
class Books(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(null=True)
    categorylist =  models.ForeignKey(CategoriesList,on_delete=models.CASCADE,null=True)
    subscription_cost = models.IntegerField(null=True)
    book_image = models.ImageField(upload_to='book_images', blank=True,null=True)

class OrdersPayment(models.Model):
    order_id = models.CharField(max_length=100,primary_key=True)
    amount = models.IntegerField(null=True)
    username = models.CharField(max_length=100,null=True)
    user_email = models.CharField(max_length=100,null=True)
    payment_id = models.CharField(max_length = 50, default = "--")
    payment_for = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PaymentProblem(models.Model):
    amount = models.IntegerField(null=True)
    username = models.CharField(max_length=100,null=True)
    user_email = models.CharField(max_length=100,null=True)
    payment_for = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)