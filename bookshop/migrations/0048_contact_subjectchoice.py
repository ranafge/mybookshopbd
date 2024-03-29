# Generated by Django 2.2.10 on 2020-07-26 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0047_auto_20200719_1244'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=250)),
                ('contact_choice_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookshop.SubjectChoice')),
            ],
        ),
    ]
