# Generated by Django 3.2.7 on 2021-10-08 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glowpick', '0005_cmkcpproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='CmkCpReview',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cmk_id', models.CharField(max_length=30)),
                ('productid', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
                ('review_create_date', models.CharField(max_length=100)),
                ('user_star', models.CharField(max_length=10)),
                ('title', models.CharField(db_column='TITLE', max_length=300)),
                ('review_content', models.TextField()),
            ],
            options={
                'db_table': 'cmk_cp_review',
                'managed': False,
            },
        ),
    ]
