# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fylke',
            fields=[
                ('nr', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('navn', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['nr'],
                'verbose_name_plural': 'Fylker',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kommune',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kode', models.CharField(max_length=4)),
                ('navn', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['kode'],
                'verbose_name_plural': 'Kommuner',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostSted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postnummer', models.CharField(max_length=4)),
                ('poststed', models.CharField(max_length=35)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lng', models.FloatField(null=True, blank=True)),
                ('kommune', models.ForeignKey(blank=True, to='dknorway.Kommune', null=True, on_delete=models.deletion.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'Poststed',
            },
            bases=(models.Model,),
        ),
    ]
