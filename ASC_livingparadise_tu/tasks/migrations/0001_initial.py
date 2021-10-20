# Generated by Django 2.0.7 on 2018-07-29 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CountBeansTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('description', models.CharField(blank=True, max_length=256, verbose_name='description')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('started_on', models.DateTimeField(null=True, verbose_name='started on')),
                ('completed_on', models.DateTimeField(null=True, verbose_name='completed on')),
                ('job_id', models.CharField(blank=True, max_length=128, verbose_name='job id')),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('RECEIVED', 'RECEIVED'), ('STARTED', 'STARTED'), ('PROGESS', 'PROGESS'), ('SUCCESS', 'SUCCESS'), ('FAILURE', 'FAILURE'), ('REVOKED', 'REVOKED'), ('REJECTED', 'REJECTED'), ('RETRY', 'RETRY'), ('IGNORED', 'IGNORED'), ('REJECTED', 'REJECTED')], db_index=True, default='PENDING', max_length=128, verbose_name='status')),
                ('mode', models.CharField(choices=[('UNKNOWN', 'UNKNOWN'), ('SYNC', 'SYNC'), ('ASYNC', 'ASYNC')], db_index=True, default='UNKNOWN', max_length=128, verbose_name='mode')),
                ('failure_reason', models.CharField(blank=True, max_length=256, verbose_name='failure reason')),
                ('progress', models.IntegerField(blank=True, null=True, verbose_name='progress')),
                ('log_text', models.TextField(blank=True, verbose_name='log text')),
                ('num_beans', models.PositiveIntegerField(default=100)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_on',),
                'get_latest_by': 'created_on',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SendEmailTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('description', models.CharField(blank=True, max_length=256, verbose_name='description')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('started_on', models.DateTimeField(null=True, verbose_name='started on')),
                ('completed_on', models.DateTimeField(null=True, verbose_name='completed on')),
                ('job_id', models.CharField(blank=True, max_length=128, verbose_name='job id')),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('RECEIVED', 'RECEIVED'), ('STARTED', 'STARTED'), ('PROGESS', 'PROGESS'), ('SUCCESS', 'SUCCESS'), ('FAILURE', 'FAILURE'), ('REVOKED', 'REVOKED'), ('REJECTED', 'REJECTED'), ('RETRY', 'RETRY'), ('IGNORED', 'IGNORED'), ('REJECTED', 'REJECTED')], db_index=True, default='PENDING', max_length=128, verbose_name='status')),
                ('mode', models.CharField(choices=[('UNKNOWN', 'UNKNOWN'), ('SYNC', 'SYNC'), ('ASYNC', 'ASYNC')], db_index=True, default='UNKNOWN', max_length=128, verbose_name='mode')),
                ('failure_reason', models.CharField(blank=True, max_length=256, verbose_name='failure reason')),
                ('progress', models.IntegerField(blank=True, null=True, verbose_name='progress')),
                ('log_text', models.TextField(blank=True, verbose_name='log text')),
                ('sender', models.CharField(max_length=256)),
                ('recipients', models.TextField(help_text='put addresses in separate rows')),
                ('subject', models.CharField(max_length=256)),
                ('message', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_on',),
                'get_latest_by': 'created_on',
                'abstract': False,
            },
        ),
    ]