# Generated by Django 3.1.7 on 2021-04-08 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0009_auto_20210408_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
