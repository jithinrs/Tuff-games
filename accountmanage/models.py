
from enum import unique
from itertools import product
from pickle import FALSE
from django.db import models
from authentications.models import Account
from products.models import Product


# Create your models here.

class useraddress(models.Model):
    id =  models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField("you name",max_length=256)
    mobile = models.CharField(max_length=32, default="1")
    email = models.CharField(max_length=140, default='1')
    address_1 = models.CharField(max_length=1024)
    address_2 = models.CharField(max_length=1024, blank=True, null=True)
    city = models.CharField(max_length=256)
    district = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    pincode = models.CharField(max_length=6)
    created_at = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "User Address"

    def __str__(self):
        return self.user_id.first_name + "'s address"    

class userpic(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    user_image = models.FileField()


class Order(models.Model):
    id =  models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    # address_id = models.ForeignKey(useraddress, on_delete = models.CASCADE)
    name = models.CharField("you name",max_length=256,null=False)
    email = models.CharField(max_length=256,null=False)
    mobile = models.CharField(max_length=256,null=False)
    address_1 = models.CharField(max_length=1024,null=False)
    address_2 = models.CharField(max_length=1024, blank=True, null=True)
    city = models.CharField(max_length=256,null=False)
    district = models.CharField(max_length=256,null=False)
    state = models.CharField(max_length=256,null=False)
    pincode = models.CharField(max_length=6,null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True, blank=True)
    orderstatus = {
        ('Order confirmed', 'Order confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Completed', 'Completed'),
        ('Order cancelled', 'Order cancelled'),
        ('Returned', 'Returned')

    }
    status = models.CharField(max_length=150, choices=orderstatus, default='Order confirmed')
    message = models.TextField(null=True, blank=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.id} - {self.tracking_no}'


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="oderuser")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productcount")
    price = models.FloatField(null=FALSE)
    quantity = models.IntegerField(null = False)

    def __str__(self):
        return f'{self.order_id.id} - {self.order_id.tracking_no}'
    

