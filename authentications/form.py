
from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Account

# Create your forms here.

class RegistrtationForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':'Enter Password'
	}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':'Enter Password'
	})) 
    class Meta:
        model=Account
        fields=['first_name','last_name' ,'email','mobile' ,'password','confirm_password']
    def clean(self):
        cleaned_data    =super(RegistrtationForm,self).clean()
        password        =cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match")    

class UserForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['is_active']
    
    def __str__(self):
        return self.first_name

class userupdateform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'mobile']