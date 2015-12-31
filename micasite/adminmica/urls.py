from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name = 'index'),
  url(r'^index', views.index, name = 'index'),
  url(r'^login', views.loginPage, name = 'login'),
  url(r'^logout',views.logoutUser, name = 'logout'),
  url(r'^getAllCategories', views.getAllCategories, name = "getAllCategories"),
  url(r'^getCategorybyID', views.getCategorybyID, name = "getCategorybyID"),
  url(r'^inventory/(?P<ID>[0-9]+|all)', views.inventory, name = "inventory"),
]
