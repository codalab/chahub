# Generated by Django 2.1.11 on 2019-11-22 01:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('producers', '0003_auto_20181218_1934'),
        ('datasets', '0005_auto_20191122_0105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote_id', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('key', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='datasets.Data')),
                ('producer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solutions', to='producers.Producer')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote_id', models.IntegerField()),
                ('created_by', models.TextField(blank=True, null=True)),
                ('creator_id', models.IntegerField(blank=True, null=True)),
                ('created_when', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('key', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('is_public', models.BooleanField(default=False)),
                ('ingestion_only_during_scoring', models.NullBooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('ingestion_program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_ingestion_programs', to='datasets.Data')),
                ('input_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_input_datas', to='datasets.Data')),
                ('producer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='producers.Producer')),
                ('reference_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_reference_datas', to='datasets.Data')),
                ('scoring_program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_scoring_programs', to='datasets.Data')),
            ],
        ),
        migrations.AddField(
            model_name='solution',
            name='tasks',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='tasks.Task'),
        ),
    ]