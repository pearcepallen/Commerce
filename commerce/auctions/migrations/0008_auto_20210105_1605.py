# Generated by Django 3.1.4 on 2021-01-05 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210105_1348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='description',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='image_link',
            new_name='image',
        ),
    ]
