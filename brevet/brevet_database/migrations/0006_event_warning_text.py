# Generated by Django 3.2.8 on 2021-12-05 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brevet_database', '0005_auto_20211205_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='warning_text',
            field=models.TextField(blank=True),
        ),
    ]