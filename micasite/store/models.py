from django.db import models
from django.core import serializers
from django.core.validators import RegexValidator
from micasite.custom_classes import SerializerMixin

class Category(models.Model, SerializerMixin):
  name = models.CharField(max_length = 100, blank = False)
  @staticmethod
  def getAllCategories():
    return serializers.serialize("json", Category.objects.all())
  @staticmethod
  def getCategory(id):
    return serializers.serialize("json", Category.objects.filter(pk__in=id)) 
  def __str__(self): 
    return self.name
  def serialize(self, exclude_list=[]):
    return serializers.serialize('json', [self])

class SubCategory(models.Model, SerializerMixin):
  name = models.CharField(max_length = 100, blank = False)
  category = models.ForeignKey(Category, on_delete = models.CASCADE)
  def __str__(self):
    return self.name

class Vendor(models.Model, SerializerMixin):
  name = models.CharField(max_length = 100, blank = False)
  address = models.CharField(max_length = 100)
  city = models.CharField(max_length = 100)
  state = models.CharField(max_length = 2)
  zip = models.IntegerField()
  description = models.TextField(blank = True)
  website_url = models.URLField()
  email = models.EmailField()
  phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message = "phone number must be entered in the format: '+999999999'")
  phone_number = models.CharField(validators=[phone_regex], blank = True, max_length = 16)
  date_joined = models.DateField()
  def __str__(self):
    return self.name

class Product(models.Model, SerializerMixin):
  name = models.CharField(max_length = 100, blank = False)
  price = models.DecimalField(decimal_places = 2, blank = False, max_digits = 6)
  sub_category = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
  vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)
  weight = models.DecimalField(decimal_places = 4, blank = True, max_digits = 8)
  description = models.TextField(blank = True);	
  updated_at = models.DateTimeField(auto_now = True, unique_for_date = True)
  created_at = models.DateTimeField(auto_now_add = True, unique_for_date = True)
  def __str__(self):
    return self.name

