# Generated by Django 3.2 on 2021-04-18 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0022_alter_answer_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer_count',
            field=models.IntegerField(default=0, null=True, verbose_name='количсество ответов на данный вопрос'),
        ),
    ]
