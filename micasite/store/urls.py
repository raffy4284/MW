from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^Vendor/$', views.getAllVendor, name = 'AllVendor'),
]
