# Generated by Django 4.0.2 on 2022-02-16 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='customer_id',
            new_name='customer',
        ),
    ]
