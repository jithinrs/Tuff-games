from dataclasses import fields
from django import forms
from .models import Categories, Product, SubCategory, Coupon, CategoryOffer, discount
# class ProductCreateForm(forms.ModelForm):
#     class Meta:
#         model = Categories
        
class ProductsAddforms(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategories_id'].queryset = SubCategory.objects.none()

class Categoryform(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['title', 'url_slug', 'thumbnail', 'description', 'is_active']


class productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['categories_id','subcategories_id','product_name','url_slug','brand','product_max_price','product_image','product_image_1','product_image_2','product_image_3','product_description','product_long_description','in_stock_total','is_active']
        

class couponform(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ['code', 'valid_from','valid_to', 'offer_value', 'active']


class couponcheck(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ['code']

class categoryoffercheck(forms.ModelForm):

    class Meta:
        model = CategoryOffer
        fields = ['category_id', 'offer_perc']

class ProductDiscountForm(forms.ModelForm):

    class Meta:
        model = discount
        fields = ['product_id', 'disc_percent']