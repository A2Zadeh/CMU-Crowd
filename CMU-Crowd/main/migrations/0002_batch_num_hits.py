# Generated by Django 2.1.7 on 2019-04-29 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='num_HITs',
            field=models.IntegerField(default=10),
        ),
    ]
