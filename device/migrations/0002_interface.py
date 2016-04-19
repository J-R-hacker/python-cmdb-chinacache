# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('if_name', models.CharField(max_length=80, null=True)),
                ('if_status', models.CharField(max_length=50, null=True)),
                ('if_OID', models.CharField(max_length=50, null=True)),
                ('if_role', models.CharField(max_length=50, null=True)),
                ('if_desc', models.CharField(max_length=200, null=True)),
                ('if_ip', models.CharField(max_length=50, null=True)),
                ('device', models.ForeignKey(to='device.Device')),
            ],
        ),
    ]
