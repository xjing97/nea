# Generated by Django 3.1.4 on 2021-02-16 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(default='', max_length=256, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GRC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grc_name', models.CharField(default='NA', max_length=256)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('user_department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='grc', to='department.userdepartment')),
            ],
            options={
                'unique_together': {('user_department', 'grc_name')},
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division_name', models.CharField(default='NA', max_length=256)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('grc', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='division', to='department.grc')),
            ],
            options={
                'unique_together': {('grc', 'division_name')},
            },
        ),
    ]
