# Generated by Django 3.1.2 on 2021-12-26 16:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20211226_0059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountbook',
            options={'ordering': ['-time']},
        ),
        migrations.AlterField(
            model_name='accountbook',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 26, 16, 27, 19, 492650, tzinfo=utc)),
        ),
    ]