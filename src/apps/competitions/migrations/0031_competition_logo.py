# Generated by Django 2.0 on 2019-01-09 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0030_auto_20190109_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
