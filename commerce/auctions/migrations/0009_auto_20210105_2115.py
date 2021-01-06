# Generated by Django 3.1.4 on 2021-01-06 02:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210105_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(default=20, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watch', to=settings.AUTH_USER_MODEL),
        ),
    ]
