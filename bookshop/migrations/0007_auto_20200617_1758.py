# Generated by Django 2.2.10 on 2020-06-17 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0006_auto_20200617_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True),
        ),
    ]