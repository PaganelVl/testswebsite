# Generated by Django 3.1.7 on 2021-04-02 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0004_auto_20210402_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='num',
            field=models.IntegerField(default=1, verbose_name='Порядковый номер'),
        ),
    ]
