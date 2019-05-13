# Generated by Django 2.2.1 on 2019-05-13 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=300)),
                ('purpose', models.TextField()),
                ('instructions', models.TextField()),
                ('active', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user_feedback', models.TextField(blank=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'survey')},
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=64)),
                ('slug', models.SlugField(blank=True)),
                ('serial_number', models.PositiveSmallIntegerField()),
                ('possitive_or_negative', models.BooleanField(default=True)),
                ('rating_type', models.BooleanField(default=False)),
                ('choice_unit', models.CharField(blank=True, max_length=12, null=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=32)),
                ('slug', models.SlugField(blank=True)),
                ('chart_text', models.CharField(blank=True, max_length=12)),
                ('serial_number', models.PositiveSmallIntegerField()),
                ('possitive_count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='portal.Choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='portal.Question')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Response')),
            ],
            options={
                'unique_together': {('question', 'response')},
            },
        ),
    ]
