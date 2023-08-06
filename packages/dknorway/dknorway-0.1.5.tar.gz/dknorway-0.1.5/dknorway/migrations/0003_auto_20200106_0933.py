# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def deactivate_fylke(Fylke, nr, new_name):
    try:
        f = Fylke.objects.get(nr=nr)
        f.active = False
        f.note = new_name
        f.save()
    except Fylke.DoesNotExist:
        pass


def new_fylke_2020(apps, schema_editor):
    Fylke = apps.get_model("dknorway", "Fylke")
    f, _ = Fylke.objects.get_or_create(nr='30', navn='Viken')
    f.note = 'Buskerud, Akershus, Østfold'
    f.save()
    f, _ = Fylke.objects.get_or_create(nr='34', navn='Innlandet')
    f.note = 'Oppland, Hedemark'
    f.save()
    f, _ = Fylke.objects.get_or_create(nr='38', navn='Vestfold og Telemark')
    f.note = 'Vestfold, Telemark'
    f.save()
    f, _ = Fylke.objects.get_or_create(nr='42', navn='Agder')
    f.note = 'Aust-Agder, Vest-Agder'
    f.save()
    f, _ = Fylke.objects.get_or_create(nr='46', navn='Vestland')
    f.note = 'Hordaland, Sogn og Fjordane'
    f.save()
    f, _ = Fylke.objects.get_or_create(nr='50', navn='Trøndelag')
    f.note = 'Sør-Trøndelag, Nord-Trøndelag'
    f.save()
    f, _ = Fylke.objects.get_or_create(nr='54', navn='Troms og Finnmark')
    f.note = 'Troms, Finnmark'
    f.save()

    deactivate_fylke(Fylke, '01', 'Viken')
    deactivate_fylke(Fylke, '02', 'Viken')
    deactivate_fylke(Fylke, '04', 'Innlandet')
    deactivate_fylke(Fylke, '05', 'Innlandet')
    deactivate_fylke(Fylke, '06', 'Viken')
    deactivate_fylke(Fylke, '07', 'Vestfold og Telemark')
    deactivate_fylke(Fylke, '08', 'Vestfold og Telemark')
    deactivate_fylke(Fylke, '09', 'Agder')
    deactivate_fylke(Fylke, '10', 'Agder')
    deactivate_fylke(Fylke, '12', 'Vestland')
    deactivate_fylke(Fylke, '14', 'Vestland')
    deactivate_fylke(Fylke, '16', 'Trøndelag')
    deactivate_fylke(Fylke, '17', 'Trøndelag')
    deactivate_fylke(Fylke, '19', 'Troms og Finnmark')
    deactivate_fylke(Fylke, '20', 'Troms og Finnmark')


class Migration(migrations.Migration):

    dependencies = [
        ('dknorway', '0002_auto_20181202_2348'),
    ]

    operations = [
        migrations.RunPython(new_fylke_2020),
    ]
