# Generated by Django 4.0 on 2022-09-08 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brevet_database', '0015_club_foreign'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
