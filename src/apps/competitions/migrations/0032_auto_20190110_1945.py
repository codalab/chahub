# Generated by Django 2.0 on 2019-01-10 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0031_competition_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='logo_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
