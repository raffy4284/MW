#!/usr/bin/env python
import os
import sys
import random
from faker import Factory
from django.core.wsgi import get_wsgi_application
if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'micasite.settings'
    application = get_wsgi_application()
    from store.models import Category, Product
    
    fake = Factory.create()
    for i in range(1,10):
        Category(name=fake.word()).save()
    categories = Category.objects.all()
    for i in range(1,1000):
        Product(
          name = fake.word(), 
          price = random.randrange(1,10000,2)+int(random.random()*100)/100.0,
          category = categories[random.randrange(1,len(categories))],
          weight = 12,
          description = fake.paragraph()
        )
