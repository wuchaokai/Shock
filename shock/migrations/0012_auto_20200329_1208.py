# Generated by Django 3.0.4 on 2020-03-29 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shock', '0011_auto_20200329_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shock_trade',
            name='cost',
            field=models.FloatField(default=0),
        ),
    ]