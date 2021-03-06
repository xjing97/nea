# Generated by Django 3.1.4 on 2020-12-17 10:45

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
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_name', models.CharField(default='', max_length=256)),
                ('description', models.TextField(blank=True, null=True)),
                ('passing_score', models.FloatField(default=50.0)),
                ('quiz_can_retake', models.BooleanField(default=False)),
                ('quiz_attempt', models.IntegerField(default=1)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('cover_image', models.ImageField(upload_to='upload/scenario')),
                ('high_rise', models.BooleanField(default=False)),
                ('level', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Easy', max_length=256)),
                ('default_config', models.TextField(default='{}')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('module_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='module.module')),
                ('user_id', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
