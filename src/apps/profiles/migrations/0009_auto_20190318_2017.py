# Generated by Django 2.1.2 on 2019-03-18 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20190318_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubuserinfo',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='events_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='followers_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='following_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='gists_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='gravatar_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='location',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='login',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='node_id',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='organizations_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='received_events_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='repos_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='starred_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='subscriptions_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='githubuserinfo',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='githubuserinfo',
            name='avatar_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='githubuserinfo',
            name='html_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='githubuserinfo',
            name='url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]