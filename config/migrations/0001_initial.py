# Generated by Django 3.1.4 on 2020-12-17 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breeding_point', models.TextField(blank=True, null=True)),
                ('is_owner_at_home', models.BooleanField(default=True)),
                ('is_owner_appeal', models.BooleanField(default=False)),
                ('is_refuse_entry', models.BooleanField(default=False)),
                ('critical_points', models.TextField(blank=True, null=True)),
                ('config', models.TextField(default='{}')),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('scenario_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='module.scenario')),
            ],
        ),
    ]
