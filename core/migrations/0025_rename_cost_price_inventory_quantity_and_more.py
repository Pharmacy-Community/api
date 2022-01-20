# Generated by Django 4.0.1 on 2022-01-15 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_alter_customer_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='cost_price',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='total',
        ),
        migrations.AddField(
            model_name='inventory',
            name='pack_cost',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='pack_size',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
