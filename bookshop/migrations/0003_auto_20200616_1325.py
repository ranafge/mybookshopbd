# Generated by Django 2.2.10 on 2020-06-16 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0002_auto_20200616_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)", max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='bookstore',
            name='edition',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='bookstore',
            name='isbn',
            field=models.CharField(default='0120120145215', help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', max_length=13, verbose_name='ISBN'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='bookstore',
            name='category',
        ),
        migrations.AddField(
            model_name='bookstore',
            name='category',
            field=models.ManyToManyField(help_text='প্রবন্ধ, গবেষণা ও অন্যান্য', max_length=150, to='bookshop.Category'),
        ),
        migrations.AddField(
            model_name='bookstore',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookshop.Language'),
        ),
    ]
