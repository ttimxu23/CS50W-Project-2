# Generated by Django 4.2.2 on 2023-06-28 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_bid_amount_alter_listing_bid_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
