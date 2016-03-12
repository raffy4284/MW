#!/usr/bin/env python
import os
import sys
import random
from faker import Factory
from django.core.wsgi import get_wsgi_application
import datetime
from datetime import date
if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'micasite.settings'
    application = get_wsgi_application()
    from django.db.models import Q
    from store.models import * 




    fake = Factory.create()
    cat = Category(name="Men")
    cat.save()
    SubCategory(name="Dress Shirts", category=cat).save()
    SubCategory(name="Shirts", category=cat).save()
    SubCategory(name="Sweaters", category=cat).save()
    SubCategory(name="Polos", category=cat).save()
    SubCategory(name="Briefs", category=cat).save()   
    SubCategory(name="Socks", category=cat).save()
    SubCategory(name="Pants", category=cat).save() 
 
    cat = Category(name="Women")
    cat.save()
    SubCategory(name="Dress", category=cat).save()
    SubCategory(name="Polos", category=cat).save()
    SubCategory(name="Sweater", category=cat).save()
    SubCategory(name="Coats", category=cat).save()
    SubCategory(name="Socks", category=cat).save()
    SubCategory(name="Panties", category=cat).save()

    cat = Category(name="Petites")
    cat.save()
    SubCategory(name="Dress", category=cat).save()
    SubCategory(name="Polos", category=cat).save()
    SubCategory(name="Sweater", category=cat).save()
    SubCategory(name="Coats", category=cat).save()
    SubCategory(name="Socks", category=cat).save()
    SubCategory(name="Panties", category=cat).save()

    Category(name="Jewelry & Accessories").save()
    Category(name="Shoes").save()

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
    sub_categories = SubCategory.objects.all()
    for i in range(1,1000):
        Product(
          name = fake.word(), 
          price = random.randrange(1,10000,2)+int(random.random()*100)/100.0,
          sub_category = sub_categories[random.randrange(0,len(sub_categories))],
          vendor = vendors[random.randrange(0,len(vendors))],
          weight = 12,
          quantity = 10,
          description = fake.paragraph()
        ).save()
    for i in range(1,1000):
        History(
          first_name = fake.first_name(),
          last_name = fake.last_name(),
          product_name = fake.word(),
          price_sold = random.randrange(1,10000,2)+int(random.random()*100)/100.0, 
          address = fake.street_address(),
          city = fake.city(),
          state = fake.state_abbr(),
          zip = random.randrange(100000,999999),
          email = fake.email(),
        ).save() 
    for i in range(1,1000):
        Order(
          first_name = fake.first_name(),
          last_name = fake.last_name(),
          price_sold = random.randrange(1,10000,2)+int(random.random()*100)/100.0, 
          address = fake.street_address(),
          city = fake.city(),
          state = fake.state_abbr(),
          zip = random.randrange(100000,999999),
          email = fake.email(),
          product = Product.objects.all()[random.randrange(1,999)],
          date_sold = date(random.randrange(2008,2016), random.randrange(1,12), random.randrange(1,28))
        ).save()
