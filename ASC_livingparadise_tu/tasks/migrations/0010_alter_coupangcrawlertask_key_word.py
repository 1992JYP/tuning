# Generated by Django 3.2.4 on 2021-09-13 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_alter_coupangcrawlertask_key_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupangcrawlertask',
            name='key_word',
            field=models.CharField(default='생활낙원', max_length=256),
        ),
    ]
