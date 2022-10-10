from dataclasses import fields
from django import forms
from .models import Categories, Product, SubCategory, Coupon
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


class couponform(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ['code', 'valid_from','valid_to', 'offer_value', 'active']


class couponcheck(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ['code']