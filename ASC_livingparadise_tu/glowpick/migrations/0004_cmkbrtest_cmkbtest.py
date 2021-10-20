# Generated by Django 3.2.7 on 2021-09-30 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glowpick', '0003_cmkcrtest'),
    ]

    operations = [
        migrations.CreateModel(
            name='CmkBrtest',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cmk_id', models.CharField(blank=True, max_length=30, null=True)),
                ('productid', models.CharField(blank=True, max_length=30, null=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('user_name', models.CharField(blank=True, max_length=30, null=True)),
                ('user_age', models.CharField(blank=True, max_length=30, null=True)),
                ('user_type', models.CharField(blank=True, max_length=50, null=True)),
                ('user_gender', models.CharField(blank=True, max_length=10, null=True)),
                ('user_star', models.CharField(blank=True, max_length=10, null=True)),
                ('review_create_date', models.CharField(blank=True, max_length=100, null=True)),
                ('review_content', models.TextField(blank=True, db_collation='utf8mb4_general_ci', null=True)),
            ],
            options={
                'db_table': 'cmk_brtest',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CmkBtest',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('cmk_id', models.CharField(blank=True, max_length=50, null=True)),
                ('second_class_name', models.CharField(blank=True, max_length=50, null=True)),
                ('gp_class', models.CharField(blank=True, max_length=50, null=True)),
                ('productid', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('ranking', models.CharField(blank=True, max_length=30, null=True)),
                ('price', models.CharField(blank=True, max_length=30, null=True)),
                ('grade', models.CharField(blank=True, max_length=30, null=True)),
                ('review_count', models.CharField(blank=True, max_length=30, null=True)),
                ('brand', models.CharField(blank=True, max_length=50, null=True)),
                ('ingredientlist', models.CharField(blank=True, max_length=5000, null=True)),
                ('detail', models.CharField(blank=True, max_length=500, null=True)),
                ('imgpath', models.CharField(blank=True, max_length=5000, null=True)),
                ('date_info', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'cmk_btest',
                'managed': False,
            },
        ),
    ]