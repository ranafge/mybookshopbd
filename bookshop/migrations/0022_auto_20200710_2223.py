# Generated by Django 2.2.10 on 2020-07-10 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0021_auto_20200710_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='payment_option',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
