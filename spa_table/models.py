from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_tables2 import tables

NULLABLE = {'blank': True, 'null': True}

class Values_table(models.Model):
    data = models.TimeField(auto_now_add=True, verbose_name='Дата')
    name = models.CharField(max_length=100, verbose_name='Название')
    quantity = models.IntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)],
                                   verbose_name='Количество')
    distance = models.IntegerField(validators=[MaxValueValidator(10000), MinValueValidator(0)],
                                   verbose_name='Расстояние')


class Values_tableTable(tables.Table):
    class Meta:
        model = Values_table


class Question(models.Model):
    body = models.CharField(max_length=300, verbose_name='Название вопроса')
    answer = models.CharField(max_length=150, verbose_name='Ответ')
    question_value = models.IntegerField(validators=[MaxValueValidator(1500), MinValueValidator(0)],
                                         verbose_name='Количество баллов за вопрос', **NULLABLE)
    created = models.TimeField(auto_now_add=True)


class QuestionTable(tables.Table):
    class Meta:
        model = Question
