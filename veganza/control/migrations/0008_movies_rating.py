# Generated by Django 2.2.1 on 2022-05-25 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0007_auto_20220523_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
