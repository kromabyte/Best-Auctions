# Generated by Django 4.0.6 on 2022-08-22 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_bids_bidder_remove_listing_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='active',
            field=models.CharField(default='active', max_length=4),
        ),
    ]
