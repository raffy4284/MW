from django import forms
from store.models import Category, Vendor, Product
from django.forms import ModelForm
from django.forms.widgets import Select

class loginForm(forms.Form):
  userName = forms.CharField(label="Username", max_length=50)
  password = forms.CharField(widget=forms.PasswordInput())

class CategoryForm(forms.Form):
  id = forms.IntegerField()

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
