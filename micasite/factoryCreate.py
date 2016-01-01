#!/usr/bin/env python
import os
import sys
import random
from faker import Factory
from django.core.wsgi import get_wsgi_application
import datetime
if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'micasite.settings'
    application = get_wsgi_application()
    from store.models import Category, Product, Vendor
    
    fake = Factory.create()
    for i in range(1,10):
        Category(name=fake.word()).save()
    for i in range(1,20):
        Vendor(
            name = fake.company(),
            address = fake.street_address(),
            city = fake.city(),
            state = fake.state_abbr(),
            zip = random.randrange(100000,999999),
            description = fake.paragraph(),
            website_url = fake.url(),
            email = fake.email(),
            date_joined = datetime.date(int(fake.year()),int(fake.month()),int(fake.day_of_month()))
        ).save()
    vendors = Vendor.objects.all()        
    categories = Category.objects.all()
    for i in range(1,1000):
        Product(
          name = fake.word(), 
          price = random.randrange(1,10000,2)+int(random.random()*100)/100.0,
          category = categories[random.randrange(0,len(categories))],
          vendor = vendors[random.randrange(0,len(vendors))],
          weight = 12,
          description = fake.paragraph()
        ).save()
