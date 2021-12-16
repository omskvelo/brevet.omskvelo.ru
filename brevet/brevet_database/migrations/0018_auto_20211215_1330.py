# Generated by Django 3.2.8 on 2021-12-15 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brevet_database', '0017_alter_route_text_brief'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='french_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='club',
            name='ACP_code',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]