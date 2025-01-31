# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 17:50
from __future__ import unicode_literals

import Map.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airline_code2', models.TextField()),
                ('lon', models.FloatField()),
                ('_id', models.TextField()),
                ('airport_icao_code', models.TextField()),
                ('num5', models.IntegerField()),
                ('typecode', models.TextField()),
                ('first_in', models.FloatField()),
                ('airline_code1', models.TextField()),
                ('lat', models.FloatField()),
                ('flight', models.TextField()),
                ('height', models.IntegerField()),
                ('num3', models.IntegerField()),
                ('airport_dep', models.TextField()),
                ('timestamp', models.TextField()),
                ('idshex', models.TextField()),
                ('str1', models.TextField()),
                ('num2', models.IntegerField()),
                ('last_modify', models.FloatField()),
                ('zone_range', Map.models.ListField(default=[])),
                ('airport_arr', models.TextField()),
                ('num1', models.IntegerField()),
                ('num4', models.IntegerField()),
                ('fid', models.TextField()),
            ],
        ),
    ]
