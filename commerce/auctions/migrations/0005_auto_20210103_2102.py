# Generated by Django 3.1.4 on 2021-01-04 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_image_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='curr_bid',
            new_name='start_bid',
        ),
    ]