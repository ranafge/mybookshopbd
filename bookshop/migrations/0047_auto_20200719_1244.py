# Generated by Django 2.2.10 on 2020-07-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0046_auto_20200718_2028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='billingaddress',
            options={'verbose_name_plural': 'Address'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
