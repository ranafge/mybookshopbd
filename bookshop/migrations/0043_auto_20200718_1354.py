# Generated by Django 2.2.10 on 2020-07-18 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0042_order_referance_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='referance_code',
            new_name='reference_code',
        ),
    ]
