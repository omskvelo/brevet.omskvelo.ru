# Generated by Django 3.2.8 on 2021-12-09 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brevet_database', '0010_event_text_intro'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='bad_roads',
            field=models.BooleanField(default=False),
        ),
    ]
