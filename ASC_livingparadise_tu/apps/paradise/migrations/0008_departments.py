# Generated by Django 3.2.4 on 2021-06-16 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paradise', '0007_delete_departments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('priority', models.IntegerField()),
            ],
            options={
                'db_table': 'departments',
                'managed': False,
            },
        ),
    ]
