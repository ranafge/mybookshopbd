# Generated by Django 2.2.10 on 2020-07-12 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0030_auto_20200712_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
