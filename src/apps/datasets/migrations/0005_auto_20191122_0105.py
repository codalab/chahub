# Generated by Django 2.1.11 on 2019-11-22 01:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('producers', '0003_auto_20181218_1934'),
        ('datasets', '0004_auto_20171222_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='data_file',
        ),
        migrations.AddField(
            model_name='data',
            name='creator_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='data',
            name='download_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='datasets', to='producers.Producer'),
        ),
        migrations.AddField(
            model_name='data',
            name='remote_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='created_by',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='created_when',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='key',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='type',
            field=models.CharField(blank=True, default='', max_length=64, null=True),
        ),
    ]
