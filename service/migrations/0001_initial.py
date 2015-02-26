# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('contrasenia', models.CharField(max_length=200)),
                ('ultima_visita', models.DateTimeField(verbose_name=b'Ultima visita')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
