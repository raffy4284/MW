#!/usr/bin/env python
import os
import sys
from django.core.wsgi import get_wsgi_application
if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'micasite.settings'
    application = get_wsgi_application()
    from store.models import Category, Product, Vendor
    for category in Category.objects.all():
        category.delete()
    for product in Product.objects.all():
        product.delete()
    for vendor in Vendor.objects.all():
        vendor.delete()
