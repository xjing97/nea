# Generated by Django 3.1.4 on 2021-01-20 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0004_auto_20201230_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario',
            name='high_rise',
        ),
        migrations.AddField(
            model_name='scenario',
            name='inspection_site',
            field=models.CharField(default='', max_length=256),
        ),
    ]
