# Generated by Django 2.2.10 on 2020-06-22 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0011_x'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookstore',
            old_name='cover_photo',
            new_name='photo',
        ),
    ]
