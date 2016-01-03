from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import loginForm, CategoryForm, EditProductForm 
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from store.models import Category, Product
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
  return render(request, 'dashboard/home.html',{})

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
    return HttpResponse(Category.getAllCategories(), content_type = 'application/json')
  else:
    return HttpResponse("404")

@user_passes_test(lambda u: u.is_superuser, login_url = "login")
def inventory(request, ID):
  if ID != "all":
    try:
      category = Category.objects.get(pk=int(ID))
      products = Product.objects.filter(category=category)
      category = category.name
      paginator = Paginator(products, 25)
    except ObjectDoesNotExist:
      return HttpResponse("404")
  else:
    category = "All Items"
    products = Product.objects.all() 
    paginator = Paginator(products,25)
  page = request.GET.get('page')
  try:
    productSet = paginator.page(page)
  except PageNotAnInteger:
    productSet = paginator.page(1)
  except EmptyPage:
    productSet = paginator.page(paginator.num_pages)
  return render(request, 'dashboard/inventory/index.html', { "category" : category, "products" : productSet })

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
      return redirect("/admin/inventory/all")
  else:
    form = EditProductForm(instance = product)
  return render(request, 'dashboard/inventory/edit.html',{ "form" : form })


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
