from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import loginForm, CategoryForm, EditProductForm, VendorForm 
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from store.models import * 
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from micasite.settings import GOOGLE_API_CLIENT_KEY
import datetime
import json

def loginPage(request):
  messages.success(request, "Log-in success!")
  messages.warning(request,"Account disabled")
  messages.error(request, "Incorrect password and/or username")
  if request.method == "POST":
    form = loginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['userName']
      password = form.cleaned_data['password']
      user = authenticate(username=username, password=password)
      if user is not None:
        if user.is_active and user.is_superuser:
          messages.set_level(request,messages.SUCCESS)
          login(request,user)
          return redirect('index')
        elif user.is_active:
          messages.set_level(request,messages.ERROR)
          return redirect(request.META.get('HTTP_REFERER'))
        else:
          messages.set_level(request,messages.WARNING)
      else:
        messages.set_level(request,messages.ERROR)
        return redirect(request.META.get('HTTP_REFERER')) 
    return render(request,'login/login.html',{'form': form})
  elif request.method == "GET":
    return render(request, 'login/login.html', {})
  return HttpResponse("404")

@user_passes_test(lambda u: u.is_superuser, login_url="login")
def index(request):
  context = {
              'order_count' : Order.objects.exclude(status="Received").count()
            } 
  return render(request, 'dashboard/home.html',context)

@csrf_exempt
def logoutUser(request):
  if request.method == "POST":
    logout(request)
    return redirect("login") 
  else:
    return HttpResponse("404")

@user_passes_test(lambda u: u.is_superuser, login_url="login")
def getCategorybyID(request):
  if request.method == "GET":
    categoryRequest = CategoryForm(request.GET)
    if categoryRequest.is_valid():
      return HttpResponse(Category.getCategory(categoryRequest['id']), content_type = 'application/json')
    else:
      return HttpResponse("Incorrect data")
  else:
    return HttpResponse("404") 

@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def getAllCategories(request):
  if request.method == "GET":
    all_categories = []
    for i in Category.objects.all():
        serialized = i.__serialize__(exclude_list = ['subcategory', 'category'])
        serialized['subcategory'] = [{'id' : sub.id, 'name' : sub.name } for sub in i.subcategory_set.all()]
        all_categories.append(serialized)   
    return JsonResponse(all_categories, safe=False)
  else:
    return HttpResponse("404")

@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def createCategory(request):
  if request.method == "POST":
    try:
      data = json.loads(request.body)
      new_category = Category(name=data['name'])
      new_category.save()
      response = HttpResponse(new_category.serialize(), content_type='application/json') 
      response['status'] = 200
      return response
    except:
      response = HttpResponse(
          content={'msg' : 'Invalid json parameter'},  
          content_type="application/json",
          status=500,
          reason="Invalid json parameter"
      )
      return response
  else:
    return HttpResponse(status=404) 

@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def inventory(request, ID):
  context = {}
  if ID == 'all':
    context['category_id'] = 'all'
    context['category_title'] = 'All'
  else:
    category = Category.objects.get(id=ID)
    context['category_id'] = category.id
    context['category_title'] = category.name
  return render(request, 'dashboard/inventory/index.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def getProducts(request,category):
  if category != "all":
    category = Category.objects.filter(name = category)
    products = Product.objects.filter(category = category)
  else:
    products = Product.objects.all()
  data = json.dumps(
  {
    "data":[
      {
        'productID' : o.id,
        'name' : o.name,
        'price' : str(o.price),
        'category' : o.category.name,
        'weight' : str(o.weight),
        'description' : o.description,
        'updated_at' : str(o.updated_at.now()),
        'created_at' : str(o.created_at.now())
      } for o in products
    ]
  })
  return HttpResponse(data, content_type = 'application/json')

@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def editInventory(request,ID):
  product = get_object_or_404(Product,pk = ID)
  if request.method == "POST":
    form = EditProductForm(request.POST, instance = product)
    if form.is_valid():
      product = form.save(commit = False)
      product.updated_at = datetime.datetime.now()
      product.save()
      messages.success(request, "Inventory item was updated successfully")    
      messages.set_level(request,messages.SUCCESS)
      return redirect("/admin/inventory/all/")
  else:
    form = EditProductForm(instance = product)
  return render(request, 'dashboard/inventory/edit.html',{"form" : form, "model" : "Product"})


@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def deleteInventory(request,ID):
  product = get_object_or_404(Product,pk=ID)
  if request.method == "POST": #temporary
    product.delete()
    messages.success(request, "Inventory item was deleted successfully")    
    messages.set_level(request,messages.SUCCESS)
    return redirect("/admin/inventory/all")
  else:
    return HttpResponse("404")

@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def editVendor(request, ID):
  vendor = get_object_or_404(Vendor, pk=ID)
  if request.method == "POST":
    form = VendorForm(request.POST, instance=vendor)
    if form.is_valid():
      vendor = form.save(commit = False)
      vendor.save()
      messages.success(request, "Vendor was updated successfully")
      messages.set_level(request, messages.SUCCESS)
      return redirect("/admin/inventory/all/")
  else:
    form = VendorForm(instance=vendor)
  return render(request, 'dashboard/inventory/edit.html', {"form" : form, "model" : "Vendor"}) 

@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def vendor(request):
  return render(request, 'dashboard/vendor/index.html', {"GOOGLE_API_KEY" : GOOGLE_API_CLIENT_KEY})

@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def history(request):
  return render(request, 'dashboard/history/index.html', {"GOOGLE_API_KEY" : GOOGLE_API_CLIENT_KEY})

@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def order(request):
  return render(request, 'dashboard/order/index.html', {"GOOGLE_API_KEY" : GOOGLE_API_CLIENT_KEY})
