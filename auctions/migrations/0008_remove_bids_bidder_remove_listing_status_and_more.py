# Generated by Django 4.0.6 on 2022-08-16 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='Bidder',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='status',
        ),
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]