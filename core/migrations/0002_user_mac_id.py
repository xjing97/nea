# Generated by Django 3.1.4 on 2020-12-23 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mac_id',
            field=models.TextField(default=''),
        ),
    ]
