# Generated by Django 4.0.1 on 2022-01-15 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_purchase_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='total',
        ),
    ]
