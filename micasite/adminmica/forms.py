from django import forms
from store.models import Category, Vendor, Product
from django.forms import ModelForm
from django.forms.widgets import Select

class loginForm(forms.Form):
  userName = forms.CharField(label="Username", max_length=50)
  password = forms.CharField(widget=forms.PasswordInput())

class CategoryForm(forms.Form):
  id = forms.IntegerField()
  name = forms.CharField(max_length=100)

class EditProductForm(ModelForm):
  class Meta:
    model = Product
    exclude = ['created_at','updated_at']
    widgets = {
      'name' : forms.TextInput(attrs={'class' : 'form-control'}),
      'price' : forms.NumberInput(attrs={'class' : 'form-control'}),
      'category': forms.Select(attrs={'class' : 'form-control'}),
      'vendor': forms.Select(attrs={'class' : 'form-control'}),
      'description' : forms.Textarea(attrs = {'class' : 'form-control', 'style' : 'resize:vertical'}),
      'weight' : forms.NumberInput(attrs = {'class' : 'form-control'})
    }

class VendorForm(ModelForm):
  class Meta:
    model = Vendor
    widgets = {
      'name' : forms.TextInput(attrs={'class' : 'form-control'}),
      'address' : forms.TextInput(attrs={'class' : 'form-control'}),
      'city' : forms.TextInput(attrs={'class' : 'form-control'}),
      'state' : forms.TextInput(attrs={'class' : 'form-control'}),
      'zip' : forms.TextInput(attrs={'class' : 'form-control'}),
      'description' : forms.Textarea(attrs={'class' : 'form-control', 'style' : 'resize:vertical'}),
      'website_url' : forms.TextInput(attrs={'class' : 'form-control'}),
      'email' : forms.TextInput(attrs={'class' : 'form-control'}),
      'phone_number' : forms.TextInput(attrs={'class' : 'form-control'}),
      'date_joined' : forms.TextInput(attrs={'class' : 'form-control'})
    }  	
