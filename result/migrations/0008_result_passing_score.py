# Generated by Django 3.1.4 on 2021-03-01 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0007_result_critical_failure'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='passing_score',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True),
        ),
    ]
