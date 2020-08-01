# Generated by Django 2.2.10 on 2020-07-27 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0048_contact_subjectchoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='text',
            field=models.TextField(max_length=250),
        ),
    ]