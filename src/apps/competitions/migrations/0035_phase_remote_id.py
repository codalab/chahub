# Generated by Django 2.1.11 on 2019-10-17 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0034_auto_20191011_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='phase',
            name='remote_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
