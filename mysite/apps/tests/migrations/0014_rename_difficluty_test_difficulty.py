# Generated by Django 3.2 on 2021-04-14 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0013_test_difficluty'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='difficluty',
            new_name='difficulty',
        ),
    ]