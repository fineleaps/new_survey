# Generated by Django 2.0 on 2019-05-13 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20190513_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='icon_class',
            field=models.CharField(default='', max_length=32),
        ),
    ]
