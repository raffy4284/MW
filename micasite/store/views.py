from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse 
from .models import * 
from adminmica.forms import *
import json

def createInvalidJsonMessage():
  return HttpResponse(
      content={'msg' : 'Invalid json parameter'},  
      content_type="application/json",
      status=500,
      reason="Invalid json parameter"
    )

def getAllOrder(request):
  json_response = {}
  json_response['data'] = []
  for i in Order.objects.all():
    serialized = i.__serialize__(exclude_list = ['product'])
    serialized['product'] = i.product.__serialize__(exclude_list = ['vendor', 'sub_category', 'order'])
    json_response['data'].append(serialized)
  return JsonResponse(json_response, safe=False) 

def getAllHistory(request):
  return JsonResponse({'data' : [history.__serialize__() for history in History.objects.all()]}, safe=False)

def getAllInventory(request, ID):
  if ID == "all":
    product_set = Product.objects.all()
  else:
    try:
      product_set = Product.objects.filter(sub_category__category__id=ID)
    except:
      return createInvalidJsonMessage()
  all_inventory = list()
  for inventory in product_set:
    inventory_serialized = inventory.__serialize__(exclude_list=['sub_category', 'vendor', 'order'])
    inventory_serialized['vendor'] = inventory.vendor.__serialize__(exclude_list=['product'])
    inventory_serialized['sub_category'] = {}
    inventory_serialized['sub_category']['name'] = inventory.sub_category.name
    inventory_serialized['sub_category']['id'] = inventory.sub_category.id
    inventory_serialized['category'] = {}
    inventory_serialized['category']['name'] = inventory.sub_category.category.name
    inventory_serialized['category']['id'] = inventory.sub_category.category.id
    all_inventory.append(inventory_serialized)
  response = { 'data' : all_inventory }
  return JsonResponse(response, safe=False)

def createEditProduct(request, ID=None):
  id_list = []
  if request.method == "POST":
    try:
      params = request.POST.getlist('data[]')
    except:
      return createInvalidJsonMessage()
  else:
    try:
      params = request.PUT.getlist('data[]')
    except:
      return createInvalidJsonMessage() 
  for index in range(0, len(params)):
    param_arrays = json.loads(params[index])
    id_list.append(param_arrays['id'])
    params[index] = EditProductForm(param_arrays)

    if params[index].is_valid():
      params[index] = params[index].cleaned_data
    else:
      error_response = {}
      error_response['fieldErrors'] = []
      for key, value in params[index].errors.iteritems():
        error_response['fieldErrors'].append({ "name" : key, "status" : value.as_text() })
      return JsonResponse(error_response, safe=False)
  if request.method == "POST":
    product_instances = [Product()]*len(params)
  else: 
    product_instances = Product.objects.filter(id__in=id_list)
  for product in product_instances:
    for data in params:
      for key, value in data.iteritems():
        if key == "sub_category":
          product.sub_category = value
        elif key == "vendor":
          product.vendor = value
        elif not hasattr(product, key):
          return createInvalidJsonMessage()
        elif key != 'id':
          setattr(product, key, value)
  for product in product_instances:
    product.save()
  json_response = {}
  json_response['data'] = []
  for product in product_instances:
    serialized = product.__serialize__(exclude_list=['vendor', 'sub_category', 'order'])
    serialized['vendor'] = product.vendor.__serialize__(exclude_list=['product'])
    serialized['sub_category'] = {}
    serialized['sub_category']['name'] = product.sub_category.name
    serialized['sub_category']['id'] = product.sub_category.id
    serialized['category'] = {}
    serialized['category']['name'] = product.sub_category.category.name
    serialized['category']['id'] = product.sub_category.category.id
    json_response['data'].append(serialized)
  return JsonResponse(json_response, safe=False)

def deleteProduct(request,ID):
  Product.objects.get(id=ID).delete()
  return JsonResponse({})

def getAllVendor(request):
  all_vendors = []
  for vendor in Vendor.objects.all():
    vendor_serialized = vendor.__serialize__(exclude_list=['product'])
    all_vendors.append(vendor_serialized)
  json_response = {"data" : all_vendors}
  return JsonResponse(json_response, safe=False) 

def createEditVendor(request, ID=None):
  id_list = []
  if request.method == "POST":
    try:
      params = request.POST.getlist('data[]')
    except:
      return createInvalidJsonMessage()
  else:
    try:
      params = request.PUT.getlist('data[]')
    except:
      return createInvalidJsonMessage() 
  for index in range(0, len(params)):
    param_arrays = json.loads(params[index])
    id_list.append(param_arrays['id'])
    params[index] = VendorForm(param_arrays)
    if params[index].is_valid():
      params[index] = params[index].cleaned_data
    else:
      error_response = {}
      error_response['fieldErrors'] = []
      for key, value in params[index].errors.iteritems():
        error_response['fieldErrors'].append({ "name" : key, "status" : value.as_text() })
      return JsonResponse(error_response, safe=False)
  if request.method == "POST":
    vendor_instances = [Vendor()]*len(params)
  else: 
    vendor_instances = Vendor.objects.filter(id__in=id_list)
  for vendor in vendor_instances:
    for data in params:
      for key, value in data.iteritems():
        if not hasattr(vendor, key):
          return createInvalidJsonMessage()
        elif key != 'id':
          setattr(vendor, key, value) 
  for vendor in vendor_instances:
    vendor.save()
  json_response = {}
  json_response['data'] = [vendor.__serialize__() for vendor in vendor_instances]
  return JsonResponse(json_response, safe=False)

def deleteVendor(request, ID):
  Vendor.objects.get(id=ID).delete()
  return JsonResponse({})


def createEditOrder(request, ID=None):
  id_list = []
  if request.method == "POST":
    try:
      params = request.POST.getlist('data[]')
    except:
      return createInvalidJsonMessage()
  else:
    try:
      params = request.PUT.getlist('data[]')
    except:
      return createInvalidJsonMessage() 
  for index in range(0, len(params)):
    param_arrays = json.loads(params[index])
    id_list.append(param_arrays['id'])
    params[index] = OrderForm(param_arrays)

    if params[index].is_valid():
      params[index] = params[index].cleaned_data
    else:
      error_response = {}
      error_response['fieldErrors'] = []
      for key, value in params[index].errors.iteritems():
        error_response['fieldErrors'].append({ "name" : key, "status" : value.as_text() })
      print error_response
      return JsonResponse(error_response, safe=False)
  if request.method == "POST":
    order_instances = [Order()]*len(params)
  else: 
    order_instances = Order.objects.filter(id__in=id_list)
  for order in order_instances:
    for data in params:
      for key, value in data.iteritems():
        if key == "product":
          order.product = value
        elif not hasattr(order, key):
          return createInvalidJsonMessage()
        elif key != 'id':
          setattr(order, key, value)
  for order in order_instances:
    order.save()
    if order.status == 'Received':
      History( 
        first_name = order.first_name,
        last_name = order.last_name,
        product_name = order.product.name,
        price_sold = order.price_sold,
        date_sold = order.date_sold,
        address = order.address,
        city = order.city,
        state = order.state,
        zip = order.zip,
        description = order.product.description,
        email = order.email,
        phone_number = order.phone_number 
      ).save()
  json_response = {}
  json_response['data'] = []
  for order in order_instances:
    serialized = order.__serialize__(exclude_list=['product'])
    serialized['product'] = order.product.__serialize__(exclude_list=['sub_category', 'vendor', 'order'])
    json_response['data'].append(serialized)
  return JsonResponse(json_response, safe=False)

def deleteOrder(request, ID):
  Order.objects.get(id=ID).delete()
  return JsonResponse({})
 
