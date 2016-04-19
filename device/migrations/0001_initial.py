# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_name', models.CharField(max_length=200)),
                ('device_ip', models.CharField(max_length=50)),
                ('device_role', models.CharField(default=b'ASW', max_length=50)),
                ('device_status', models.CharField(max_length=200)),
                ('device_uplinkoid', models.CharField(default=b'None', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Manu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Manu', models.CharField(max_length=80, null=True)),
                ('dtype', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_name', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='manu',
            field=models.ForeignKey(to='device.Manu'),
        ),
        migrations.AddField(
            model_name='device',
            name='node',
            field=models.ForeignKey(to='device.Node'),
        ),
    ]
