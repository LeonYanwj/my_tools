# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-23 08:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=16)),
                ('ipaddr', models.GenericIPAddressField()),
                ('uptime', models.CharField(max_length=16)),
                ('cpustat', models.CharField(max_length=16)),
                ('memory', models.CharField(max_length=16)),
                ('rootdisk', models.CharField(max_length=16)),
                ('iostat', models.FloatField()),
                ('network', models.BooleanField(default=True)),
                ('ms', models.CharField(max_length=16)),
                ('createdate', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '主机状态列表',
            },
        ),
        migrations.CreateModel(
            name='HostType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typename', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name_plural': '主机所属区域',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=16)),
                ('code', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'verbose_name_plural': '用户列表',
            },
        ),
        migrations.AddField(
            model_name='hostinfo',
            name='hosttype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managehost.HostType'),
        ),
    ]
