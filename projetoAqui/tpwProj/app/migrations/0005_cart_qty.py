# Generated by Django 3.1 on 2020-11-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20201121_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='qty',
            field=models.PositiveIntegerField(default=0),
        ),
    ]