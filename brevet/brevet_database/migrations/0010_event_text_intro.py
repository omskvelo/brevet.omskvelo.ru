# Generated by Django 3.2.8 on 2021-12-09 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brevet_database', '0009_route_map_embed_src'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='text_intro',
            field=models.TextField(blank=True),
        ),
    ]
