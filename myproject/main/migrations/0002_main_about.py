# Generated by Django 3.1.3 on 2020-12-03 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='about',
            field=models.TextField(default='-'),
        ),
    ]