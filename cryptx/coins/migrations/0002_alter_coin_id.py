# Generated by Django 3.2.8 on 2021-10-18 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]