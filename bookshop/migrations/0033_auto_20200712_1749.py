# Generated by Django 2.2.10 on 2020-07-12 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0032_auto_20200712_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookshop.Coupon'),
        ),
    ]
