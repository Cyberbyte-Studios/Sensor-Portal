# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-14 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0005_axis_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='metric',
            name='x_axis',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='metric',
            name='y_axis',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
