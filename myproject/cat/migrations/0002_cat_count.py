# Generated by Django 3.1.3 on 2020-12-08 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]