# Generated by Django 3.2 on 2021-04-10 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0010_auto_20210408_1419'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='text',
            new_name='text_answer',
        ),
        migrations.AlterField(
            model_name='answer',
            name='num',
            field=models.IntegerField(default=1, verbose_name='Порядковый номер'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tests.question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='question',
            name='num',
            field=models.IntegerField(default=1, verbose_name='Порядковый номер'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Никнейм пользователя'),
        ),
    ]
