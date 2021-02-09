from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserLogin(models.Model):
    email     = models.CharField(max_length=200)
    password  = models.CharField(max_length=200)

class UserDetails(models.Model):
    name       = models.CharField(max_length=200)
    number     = models.CharField(max_length=200)
    address    = models.CharField(max_length=200)
    city       = models.CharField(max_length=200)
    state      = models.CharField(max_length=200)
    country    = models.CharField(max_length=200)
    zipcode    = models.CharField(max_length=200)
    fk_username= models.ForeignKey(UserLogin,on_delete=models.CASCADE,default=None)

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(UserLogin, on_delete=models.SET_NULL, blank=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
