# Generated by Django 4.2.2 on 2023-06-28 00:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_bid_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='wishlisted',
            field=models.ManyToManyField(blank=True, related_name='wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
