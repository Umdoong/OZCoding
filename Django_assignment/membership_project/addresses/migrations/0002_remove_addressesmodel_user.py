# Generated by Django 5.1.4 on 2024-12-10 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addressesmodel',
            name='user',
        ),
    ]
