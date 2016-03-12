# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-12 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(b'Pennding', b'Pending'), (b'Processed', b'Processed'), (b'Shipped', b'Shipped'), (b'Received', b'Received'), (b'Returned', b'Returned')], default=b'Pending', max_length=9),
        ),
    ]
