import requests
import names
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import SingleTableView
from spa_table.models import Values_tableTable, Values_table, Question
from random import randint


class TableListView(SingleTableView):
    model = Values_table
    table_class = Values_tableTable
    for i in range(1, 10):
        values = Values_table.objects.create(
            name=names.get_last_name(),
            quantity=randint(1, 100),
            distance=randint(1, 100),
        )
        values.save()
    print('___________2_____________')

    queryset = Values_table.objects.all()
    template_name = "spa_table/Values_table_list.html"
    ordering = ('distance',)  # quantity, name
    table_pagination = {"per_page": 5}

    def get_queryset(self, **kwargs):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.request.method == "GET":

            if self.queryset is not None:
                queryset = self.queryset
                if isinstance(queryset, QuerySet):
                    queryset = queryset.all()
            if self.model is not None:
                queryset = self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
                )
            ordering = self.get_ordering()
            if ordering:
                if isinstance(ordering, str):
                    ordering = (ordering,)
                queryset = queryset.order_by(*ordering)
        Values_table.objects.all().delete()

        for i in range(1, 5):
            values = Values_table.objects.create(
                name=names.get_last_name(),
                quantity=randint(1, 100),
                distance=randint(1, 100), )
            values.save()
        queryset = Values_table.objects.all()

        return queryset


from django import forms


class NumberQuestion(forms.Form):
    number = forms.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)], )


########### def render_api_question(request): class Values_tableListView(ListView): Odno i to zhe delaut#################
def render_api_question(request):

    number_form = NumberQuestion(request.POST)
    queryset = {'object_list': Question.objects.all,
                'number_form': number_form}
    if request.method == "POST":
        # form = NumberQuestion(request.POST)
        if number_form.is_valid():
            c = number_form['number'].value()
            url = f'https://jservice.io/api/random?count={c}'
            response = requests.get(
                url,
                params={'count': f'{c}'},
            )
            if response.status_code == 200:
                a = response.json()
                for i in range(0, int(c)):
                    values = Question.objects.create(
                        body=a[i].get('question'),
                        answer=a[i].get('answer'),
                        question_value=a[i].get('value'), )
                    print('values.body', values.body)
                    if proverka_unik(values.body):
                        raise ValueError("Вопроc уже был")
                    values.save()

        else:
            number_form = NumberQuestion()
            # print('An error has occurred.')

    return render(request, 'spa_table/home.html', queryset)

# def render_api_question(request):
#     global number
#
#     queryset = {'object_list': Question.objects.all}
#     if request.method == "POST":
#         url = f'https://jservice.io/api/random?count={number}'
#         response = requests.get(
#             url,
#             params={'count': 1},
#             # headers={'Accept': 'application/vnd.github.v3.text-match+json'},
#         )
#         if response.status_code == 200:
#             a = response.json()
#             values = Question.objects.create(
#                 body=a[0].get('question'),
#                 answer=a[0].get('answer'),
#                 question_value=a[0].get('value'), )
#             print('values.body', values.body)
#             # proverka_unik(values.body)
#             ###############################################
#             # Nuzhna proverka na unikalnost voprosa
#             ##############################################
#             values.save()
#
#         else:
#             print('An error has occurred.')
#         return render(request, 'spa_table/home.html', queryset)
#     return render(request, 'spa_table/home.html', queryset)
# <form action="/login/" method="POST">
#   <input type="text" name="keyword" placeholder="Search query">
#   <input type="number" name="results" placeholder="Number of results">
# </form>
############Email to send this task
# hr@bewise.ai
#######################################3
def proverka_unik(a: str):
    HH = []
    H = Question.objects.all()
    index = 0
    try:
        question = Question.objects.get(pk=1).body
    except Question.DoesNotExist:
        question = None
    # print(question)
    while len(H)-index > 1:
        for i in range(len(H)):
            try:
                HH.append(question)
            except Question.DoesNotExist:
                question = None
            index += 1
        if a in HH:
            return True
        return False


# class Values_tableListView(ListView):
#     model = Values_table
#     template_name = 'spa_table/home.html'

 # <input type="number" value="{{number}}"  placeholder="Number of questions">

# https://faint-adasaurus-4bc.notion.site/web-Python-adf33211e9cc4d6b9ec2c0c619ecab31
