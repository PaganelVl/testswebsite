# Generated by Django 3.2 on 2021-04-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0016_alter_test_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='difficulty',
            field=models.CharField(choices=[('легко', 'легко'), ('средне', 'средне'), ('тяжело', 'тяжело')], default='', max_length=6, verbose_name='Сложность'),
        ),
    ]