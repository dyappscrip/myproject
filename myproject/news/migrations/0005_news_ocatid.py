# Generated by Django 3.1.3 on 2020-12-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_news_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='ocatid',
            field=models.IntegerField(default=0),
        ),
    ]