# Generated by Django 2.2.10 on 2020-07-10 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0020_auto_20200710_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='total_amount',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]