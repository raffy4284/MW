from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse 
from .models import Vendor

def getAllVendor(request):
  all_vendors = [vendor.__serialize__() for vendor in Vendor.objects.all()]
  json_response = {"data" : all_vendors}
  return JsonResponse(json_response, safe=False) 
