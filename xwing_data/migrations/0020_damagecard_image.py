# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-25 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xwing_data', '0019_auto_20170330_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='damagecard',
            name='image',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
