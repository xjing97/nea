# Generated by Django 3.1.4 on 2021-01-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0002_auto_20210111_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='config',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='mac_id',
            field=models.CharField(default='', max_length=256),
        ),
    ]
