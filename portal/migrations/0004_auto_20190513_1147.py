# Generated by Django 2.0 on 2019-05-13 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20190513_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='choice_unit',
            field=models.CharField(default='', max_length=12),
        ),
    ]
