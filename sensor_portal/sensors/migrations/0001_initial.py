# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 22:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nexmo', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=5)),
                ('eu_limit', models.IntegerField(blank=True, null=True, verbose_name='EU Concentration Limits')),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('recorded', models.DateTimeField()),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nexmo.Message')),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensors.Metric')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', geoposition.fields.GeopositionField(blank=True, max_length=42, null=True)),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='reading',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensors.Site'),
        ),
    ]
