# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('mobile', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('is_taxable', models.BooleanField(default=False)),
                ('invoice_date', models.DateField(auto_now_add=True)),
                ('invoice_number', models.CharField(max_length=10, unique=True)),
                ('date_of_supply', models.DateField()),
                ('place_of_supply', models.CharField(blank=True, max_length=50, null=True)),
                ('transport_mode', models.CharField(blank=True, max_length=200, null=True)),
                ('vehicle_number', models.CharField(blank=True, max_length=100, null=True)),
                ('total_before_tax', models.DecimalField(default=0, decimal_places=2, max_digits=12)),
                ('cgst', models.DecimalField(default=0, decimal_places=2, max_digits=10)),
                ('sgst', models.DecimalField(default=0, decimal_places=2, max_digits=10)),
                ('igst', models.DecimalField(default=0, decimal_places=2, max_digits=10)),
                ('total_after_tax', models.DecimalField(default=0, decimal_places=2, max_digits=12)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('is_cleared', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(to='Software.Agent', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=120)),
                ('address', models.CharField(blank=True, max_length=300, null=True, default=None)),
                ('mobile', models.CharField(blank=True, max_length=50, null=True)),
                ('gstin', models.CharField(blank=True, max_length=30, null=True)),
                ('debit_balance', models.DecimalField(blank=True, default=0.0, decimal_places=2, max_digits=10)),
                ('state_code', models.CharField(blank=True, max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('rate', models.DecimalField(default=0.0, decimal_places=2, max_digits=10)),
                ('qty', models.DecimalField(default=0, decimal_places=0, max_digits=10)),
                ('bill', models.ForeignKey(to='Software.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('paid_amount', models.DecimalField(default=0, decimal_places=2, max_digits=12)),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('method_of_payment', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('is_cleared', models.BooleanField(default=False)),
                ('client', models.ForeignKey(to='Software.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('hsn_code', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(to='Software.Product'),
        ),
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.ForeignKey(to='Software.Size'),
        ),
        migrations.AddField(
            model_name='bill',
            name='client',
            field=models.ForeignKey(to='Software.Client'),
        ),
    ]
