# Generated by Django 3.1.3 on 2020-12-30 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangolearn', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='test',
        ),
    ]
