from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^Category/(?P<ID>[0-9]+|all)/Inventory/$', views.getAllInventory, name = 'AllInventory'),
  url(r'^Inventory/create/$', views.createEditProduct, name='CreateProduct'),
  url(r'^Inventory/edit/(?P<ID>[0-9]+)/$', views.createEditProduct, name='EditProduct'),
  url(r'^Inventory/delete/(?P<ID>[0-9]+)/$', views.deleteProduct, name="DeleteProduct"),
  url(r'^Vendor/$', views.getAllVendor, name = 'AllVendor'),
  url(r'^Vendor/create/$', views.createEditVendor, name='CreateVendor'),
  url(r'^Vendor/edit/(?P<ID>[0-9]+)/$',  views.createEditVendor, name='EditVendor'),
  url(r'^Vendor/delete/(?P<ID>[0-9]+)/$', views.deleteVendor, name='DeleteVendor')
]
