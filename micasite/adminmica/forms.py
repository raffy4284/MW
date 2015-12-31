from django import forms

class loginForm(forms.Form):
  userName = forms.CharField(label="Username", max_length=50)
  password = forms.CharField(widget=forms.PasswordInput())

class CategoryForm(forms.Form):
  id = forms.IntegerField()
