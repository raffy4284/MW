#!/usr/bin/env python
import os
import sys
from django.core.wsgi import get_wsgi_application
if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'micasite.settings'
    application = get_wsgi_application()
    from store.models import *
    SubCategory.objects.all().delete()
    Category.objects.all().delete()
    Product.objects.all().delete()
    Vendor.objects.all().delete()
