# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 22:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceline',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
