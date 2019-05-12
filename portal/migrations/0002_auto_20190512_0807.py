# Generated by Django 2.2.1 on 2019-05-12 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='serial_number',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='survey',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='choice',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('my_session', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='portal.MySession')),
            ],
        ),
        migrations.RemoveField(
            model_name='answer',
            name='my_session',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='unique_id',
        ),
        migrations.AddField(
            model_name='answer',
            name='response',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='portal.Response'),
            preserve_default=False,
        ),
    ]
