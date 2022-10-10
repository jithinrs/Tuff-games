from dataclasses import field
from django import forms
from .models import  Order, useraddress


class addressform(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Name'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Phone Number'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Email'}))
    address_1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    address_2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    district = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = useraddress
        fields = ['name', 'address_1', 'address_2', 'city', 'district', 'state', 'pincode', 'mobile', 'email', 'user_id']




class addresscheckform(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Name'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Phone Number'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Email'}))
    address_1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    address_2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    district = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = useraddress
        fields = ['name', 'address_1', 'address_2', 'city', 'district', 'state', 'pincode', 'mobile', 'email']
    


class newstatus(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status']



    