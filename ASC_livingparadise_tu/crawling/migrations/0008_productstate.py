# Generated by Django 3.2.4 on 2021-09-03 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0007_nvproduct_nvreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pd_manager', models.CharField(db_column='PD_MANAGER', max_length=30)),
                ('pd_code', models.CharField(db_column='PD_CODE', max_length=30)),
                ('pd_name', models.CharField(db_column='PD_NAME', max_length=50)),
                ('pd_state', models.CharField(db_column='PD_STATE', max_length=20)),
                ('pd_review_count', models.IntegerField(db_column='PD_REVIEW_COUNT')),
                ('pd_price', models.IntegerField(db_column='PD_PRICE')),
                ('pd_grade', models.IntegerField(db_column='PD_GRADE')),
            ],
            options={
                'db_table': 'PRODUCT_STATE',
                'managed': False,
            },
        ),
    ]
