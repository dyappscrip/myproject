# Generated by Django 3.1.3 on 2020-12-03 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20201203_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]