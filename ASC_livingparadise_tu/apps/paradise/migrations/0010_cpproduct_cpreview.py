# Generated by Django 3.2.4 on 2021-06-18 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paradise', '0009_auto_20210617_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CpProduct',
            fields=[
                ('pd_index', models.IntegerField(db_column='PD_INDEX')),
                ('keyword', models.CharField(db_column='KEYWORD', max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(db_column='TITLE', max_length=200)),
                ('page_link', models.CharField(db_column='PAGE_LINK', max_length=200)),
                ('product_id', models.CharField(db_column='PRODUCT_ID', max_length=20)),
                ('price', models.IntegerField(db_column='PRICE')),
                ('review_count', models.IntegerField(db_column='REVIEW_COUNT')),
                ('image_link', models.CharField(db_column='IMAGE_LINK', max_length=200)),
                ('item_id', models.CharField(db_column='ITEM_ID', max_length=20)),
            ],
            options={
                'db_table': 'CP_PRODUCT',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CpReview',
            fields=[
                ('product_id', models.CharField(db_column='PRODUCT_ID', max_length=20, primary_key=True, serialize=False)),
                ('user_name', models.CharField(db_column='USER_NAME', max_length=20)),
                ('review_date', models.CharField(db_column='REVIEW_DATE', max_length=10)),
                ('score', models.IntegerField(db_column='SCORE')),
                ('product_name', models.CharField(db_column='PRODUCT_NAME', max_length=200)),
                ('review_text', models.CharField(db_column='REVIEW_TEXT', max_length=500)),
            ],
            options={
                'db_table': 'CP_REVIEW',
                'managed': False,
            },
        ),
    ]
