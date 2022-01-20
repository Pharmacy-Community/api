# Generated by Django 4.0.1 on 2022-01-15 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_purchase_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=13, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
