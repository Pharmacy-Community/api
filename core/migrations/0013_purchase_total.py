# Generated by Django 4.0.2 on 2022-02-07 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_account_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='total',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
