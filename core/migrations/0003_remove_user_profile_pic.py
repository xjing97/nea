# Generated by Django 3.1.4 on 2020-12-24 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user_mac_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_pic',
        ),
    ]
