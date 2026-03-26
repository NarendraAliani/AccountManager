# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Software', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='discount',
            field=models.DecimalField(max_digits=10, default=0, decimal_places=2),
        ),
        migrations.AddField(
            model_name='bill',
            name='qty_total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
