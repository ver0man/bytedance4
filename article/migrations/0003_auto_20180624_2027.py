# Generated by Django 2.0.5 on 2018-06-24 20:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('article', '0002_auto_20180617_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now,
                                       verbose_name='time created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='images',
            name='last_modified_time',
            field=models.DateTimeField(auto_now=True, verbose_name='time last modified'),
        ),
    ]
