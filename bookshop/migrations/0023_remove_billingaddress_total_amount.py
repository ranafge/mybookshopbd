# Generated by Django 2.2.10 on 2020-07-11 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0022_auto_20200710_2223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='total_amount',
        ),
    ]