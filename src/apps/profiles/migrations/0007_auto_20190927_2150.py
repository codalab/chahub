# Generated by Django 2.1.7 on 2019-09-27 21:50

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('producers', '0003_auto_20181218_1934'),
        ('profiles', '0006_auto_20170831_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountMergeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master_key', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('secondary_key', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('master_confirmation', models.BooleanField(default=False)),
                ('secondary_confirmation', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('emails_sent', models.BooleanField(default=False)),
                ('master_email', models.EmailField(max_length=254)),
                ('secondary_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('verified', models.BooleanField(default=False)),
                ('primary', models.BooleanField(default=False)),
                ('verification_key', models.UUIDField(default=uuid.uuid4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GithubUserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=30, unique=True)),
                ('login', models.CharField(blank=True, max_length=100, null=True)),
                ('avatar_url', models.URLField(blank=True, max_length=100, null=True)),
                ('gravatar_id', models.CharField(blank=True, max_length=100, null=True)),
                ('html_url', models.URLField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('bio', models.TextField(blank=True, max_length=2000, null=True)),
                ('location', models.CharField(blank=True, max_length=120, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('node_id', models.CharField(default='', max_length=50, unique=True)),
                ('url', models.URLField(blank=True, max_length=100, null=True)),
                ('followers_url', models.URLField(blank=True, max_length=100, null=True)),
                ('following_url', models.URLField(blank=True, max_length=100, null=True)),
                ('gists_url', models.URLField(blank=True, max_length=100, null=True)),
                ('starred_url', models.URLField(blank=True, max_length=100, null=True)),
                ('subscriptions_url', models.URLField(blank=True, max_length=100, null=True)),
                ('organizations_url', models.URLField(blank=True, max_length=100, null=True)),
                ('repos_url', models.URLField(blank=True, max_length=100, null=True)),
                ('events_url', models.URLField(blank=True, max_length=100, null=True)),
                ('received_events_url', models.URLField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote_id', models.IntegerField()),
                ('username', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('details', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('scrubbed', models.BooleanField(default=False)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='producers.Producer')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_url',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='user',
            name='company',
        ),
        migrations.RemoveField(
            model_name='user',
            name='github_uid',
        ),
        migrations.RemoveField(
            model_name='user',
            name='html_url',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='url',
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='github_user_info', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='emailaddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_addresses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accountmergerequest',
            name='master_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_merge_requests', to='profiles.EmailAddress'),
        ),
        migrations.AddField(
            model_name='accountmergerequest',
            name='secondary_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secondary_merge_requests', to='profiles.EmailAddress'),
        ),
        migrations.AlterUniqueTogether(
            name='profile',
            unique_together={('remote_id', 'producer')},
        ),
        migrations.AlterUniqueTogether(
            name='accountmergerequest',
            unique_together={('master_account', 'secondary_account')},
        ),
    ]