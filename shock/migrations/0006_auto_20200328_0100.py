# Generated by Django 3.0.4 on 2020-03-27 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shock', '0005_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='code',
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=0, max_length=200),
        ),
    ]