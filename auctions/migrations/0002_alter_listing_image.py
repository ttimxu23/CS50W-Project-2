# Generated by Django 4.2.2 on 2023-06-24 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, height_field=250, null=True, upload_to='images/'),
        ),
    ]
