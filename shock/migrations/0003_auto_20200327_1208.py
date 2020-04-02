# Generated by Django 3.0.4 on 2020-03-27 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shock', '0002_auto_20200326_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShockList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='shockinfo',
            old_name='maket',
            new_name='market',
        ),
    ]