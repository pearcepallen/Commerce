# Generated by Django 3.1.4 on 2021-01-07 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_auto_20210107_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_bid', to='auctions.listing'),
        ),
    ]
