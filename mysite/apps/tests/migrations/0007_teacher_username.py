# Generated by Django 3.1.7 on 2021-04-06 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0006_auto_20210403_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Никнейм пользователя'),
        ),
    ]
