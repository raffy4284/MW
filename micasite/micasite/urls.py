from django.conf.urls import include, url
#from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include('adminmica.urls')),
]
