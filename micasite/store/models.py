from django.db import models
from django.core import serializers

class Category(models.Model):
  name = models.CharField(max_length = 100, blank = False)
  @staticmethod
  def getAllCategories():
    return serializers.serialize("json", Category.objects.all())
  @staticmethod
  def getCategory(id):
    return serializers.serialize("json", Category.objects.filter(pk__in=id)) 
  def __str__(self): 
    return self.name

class Product(models.Model):
  name = models.CharField(max_length = 100, blank = False)
  price = models.DecimalField(decimal_places = 2, blank = False, max_digits = 6)
  category = models.ForeignKey(Category, on_delete = models.CASCADE)
  weight = models.DecimalField(decimal_places = 4, blank = True, max_digits = 8)
  description = models.TextField(blank = True);	
  updated_at = models.DateTimeField(auto_now = True, unique_for_date = True)
  created_at = models.DateTimeField(auto_now_add = True, unique_for_date = True)
  def __str__(self):
    return self.name

