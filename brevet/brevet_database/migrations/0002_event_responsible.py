# Generated by Django 3.2.8 on 2021-12-01 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brevet_database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='responsible',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]