# Generated by Django 3.0.4 on 2020-03-28 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shock', '0008_auto_20200328_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='shock_trade',
            name='shock_name',
            field=models.CharField(default=0, max_length=200),
        ),
        migrations.AlterField(
            model_name='shock_trade',
            name='code',
            field=models.CharField(default=0, max_length=200),
        ),
    ]