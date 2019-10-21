# Generated by Django 2.1.11 on 2019-10-18 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('producers', '0003_auto_20181218_1934'),
        ('competitions', '0037_competitionparticipant_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionparticipant',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='competition_participants', to='producers.Producer'),
        ),
    ]
