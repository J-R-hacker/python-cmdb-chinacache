# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insubnet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subnet_id', models.CharField(max_length=100)),
                ('subnet_mask', models.CharField(max_length=100)),
                ('subnet_status', models.CharField(max_length=50)),
                ('subnet_fornode', models.CharField(max_length=100)),
            ],
        ),
    ]
