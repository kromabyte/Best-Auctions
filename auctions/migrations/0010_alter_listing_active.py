# Generated by Django 4.0.6 on 2022-08-23 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_listing_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
