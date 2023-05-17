# Generated by Django 4.2.1 on 2023-05-17 07:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spa_table', '0002_rename_table_values_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200, verbose_name='Название вопроса')),
                ('answer', models.CharField(max_length=100, verbose_name='Ответ')),
                ('question_value', models.IntegerField(validators=[django.core.validators.MaxValueValidator(1500), django.core.validators.MinValueValidator(0)], verbose_name='Количество баллов за вопрос')),
                ('created', models.TimeField(auto_now_add=True)),
            ],
        ),
    ]
