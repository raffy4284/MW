from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import loginForm, CategoryForm 
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from store.models import Category, Product
from django.core.exceptions import ObjectDoesNotExist

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
      category = Category.objects.get(pk=int(ID)).name #fix! must account for non-existing id's
    except ObjectDoesNotExist:
      return HttpResponse("404")
  else:
    category = "All Items"
  return render(request, 'dashboard/inventory.html', { "category" : category })
