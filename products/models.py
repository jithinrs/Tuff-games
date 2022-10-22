from email import message
from email.policy import default
from unicodedata import category
from xml.dom import ValidationErr
from django.db import models
from django.urls import reverse
from authentications.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

# class TitleManager(models.Manager):
#     def Validate(self, title):
#         x = title.title()
#         catgeory = Categories.objects.create(
#             title = x
#         )
            # error_messages = { "unique":"The Geeks Field you entered is not unique."}


class Categories(models.Model):
    id =  models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=255, unique=True)
    url_slug = models.SlugField(max_length=255, unique=True)
    category_offer =models.IntegerField(default = 0, null = True, blank = True ,validators = [MinValueValidator(0), MaxValueValidator(50)])
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    # objects = TitleManager()

    class Meta():
        verbose_name_plural = "Categories"
        # unique_together = [['title']]

    # def save(self, force_insert=False, force_update=False):
    #     self.title = self.title.title() 
    #     super(Categories, self).save(force_insert, force_update)

    # def clean(self):
    #     cleaned_data = self.cleaned_data['title']
    #     print(cleaned_data)
    #     title = cleaned_data.get('title')
    #     if Categories.objects.filter(title = title).exists():
    #         raise ValidationErr('please enter another name')

    # def save(self, *args, **kwargs):
    #     try:
    #         self.title = self.title.title()
    #         return super().save(*args, **kwargs)
    #     except:
    #         return 

            


    def get_absolute_url(self): 
        return reverse('categorylist')

    def __str__(self):
        return self.title

# def clean(self):
#     cleaned_data = super(Categories,self).clean()
#     print(cleaned_data)
#     title = cleaned_data.get('title')
#     if Categories.objects.filter(title = title).exists():
#         raise ValueError('please enter another name')

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='subcategories')
    title = models.CharField(max_length=255)
    url_slug = models.SlugField(max_length=255, unique=True)
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self): 
        return reverse('subcategoryfulllist')
    
    # def get_suburl(self):
    #     return reverse('shopcat', args=[self.category_id.url_slug, self.url_slug])

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    categories_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    subcategories_id = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    url_slug = models.SlugField(max_length=255, unique=True)
    brand = models.CharField(max_length=255)
    product_offer = models.IntegerField(null = True, blank = True , default = 0, validators = [MinValueValidator(0), MaxValueValidator(50)])
    product_max_price = models.CharField(max_length=255)
    product_image = models.FileField()
    product_image_1 = models.FileField(default='')
    product_image_2 = models.FileField(default='')
    product_image_3 = models.FileField(default='')
    product_description = models.TextField()
    product_long_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    in_stock_total = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self): 
        return reverse('productlist')
    
    # def get_absolute_url(self):
    #     return reverse('store:product_detail', args=[self.slug])

    def get_userside_url(self):
        return reverse('productview', args=[self.categories_id.url_slug, self.subcategories_id.url_slug, self.url_slug])

    def get_adminside_url(self):
        return reverse('singleproduct', args=[self.categories_id.url_slug, self.subcategories_id.url_slug, self.url_slug])

    def get_suburl(self):
        return reverse('shopcat', args=[self.categories_id.url_slug, self.subcategories_id.url_slug])
    
    def discountprice(self):
        return int(self.product_max_price) * (1 - int(self.product_offer)/100)
    

# class Cartmodel(models.Model):
#     id = models.AutoField(primary_key=True)
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    coupon_val = models.IntegerField(null = True, blank = True)

    def __str__(self):
        try:
            return self.user.first_name + "'s cart - " + self.product.product_name
        except:
            return "guest's cart - " + self.product.product_name
    
    def total_price(self):
        return int(self.product_qty * int(self.product.product_max_price))

    def total_discount_price(self):
        discount_value = int(self.product.product_max_price) * (1 - int(self.product.product_offer)/100)
        return int(self.product_qty * discount_value)
    
    def whichoffer(self):
        product_offers = int(self.product.product_offer)
        category_offers = int(self.product.categories_id.category_offer)

        if product_offers > 0 or category_offers > 0:
            return 1
        else:
            return 0
        
    
    def best_offer(self):

        product_offers = int(self.product.product_offer)
        category_offers = int(self.product.categories_id.category_offer)
        if product_offers > 0 or category_offers > 0 :

            if product_offers > category_offers:
                discount_price = int(self.product.product_max_price) * (1 - int(product_offers)/100)
                return int(self.product_qty * discount_price)
            else:
                discount_price = int(self.product.product_max_price) * (1 - int(category_offers)/100)
                return int(self.product_qty * discount_price)
        
        else:
            return int(self.product_qty * int(self.product.product_max_price))







    

class Specification(models.Model):
    product_id =  models.ForeignKey(Product, on_delete=models.CASCADE, related_name="spec_details")
    spec_title = models.TextField(max_length=255)
    spec_description = models.TextField()

    def __str__(self):
        return self.spec_title

    def get_absolute_url(self): 
        return reverse('productlist')

class discount(models.Model):
    product_id =  models.ForeignKey(Product, on_delete=models.CASCADE, related_name="disc_details")
    # cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    disc_percent = models.IntegerField()


    # def __str__(self):
    #     return self.product_id
    def __str__(self):
        return self.product_id.product_name + " " + str(self.disc_percent) + "% discount"

    def discountprice(self):
        return int(self.product_id.product_max_price) * (1 - int(self.disc_percent)/100)

   
class wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)




class NewCart(models.Model):
    cart_id = models.CharField(max_length = 250, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    


class NewCartItem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    newcart_id = models.ForeignKey(NewCart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_id

class Coupon(models.Model):
    code = models.CharField(max_length = 50,unique = True)
    valid_from = models.DateField()
    valid_to = models.DateField()

    offer_value = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(70)])

    active = models.BooleanField()

    def get_absolute_url(self): 
        return reverse('couponshow')

    def __str__(self):
        return self.code

class Couponuser(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    coupon_modal = models.ForeignKey(Coupon, on_delete = models.CASCADE, null = True, blank = True)
    coupon_code = models.CharField(max_length = 50, null = True, blank = True)
    coupon_value = models.IntegerField(null = True, blank = True)


class CategoryOffer(models.Model):
    category_id = models.ForeignKey(Categories, on_delete = models.CASCADE, null = True, related_name = 'catoffer')
    offer_perc = models.IntegerField()