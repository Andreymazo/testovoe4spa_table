import requests
import names
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import SingleTableView
from spa_table.models import Values_tableTable, Values_table, Question
from random import randint


class TableListView(SingleTableView):  #
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


########### def render_api_question(request): class Values_tableListView(ListView): Odno i to zhe delaut#################
def render_api_question(request):
    queryset = {'object_list': Question.objects.all}
    response = requests.get(
        'https://jservice.io/api/random?count=1',
        params={'count': 1},
        # headers={'Accept': 'application/vnd.github.v3.text-match+json'},
    )
    if response.status_code == 200:
        a = response.json()
        print('aaaaaaaaaaaaaaaaaa', a[0].get('answer'))#aaaaaaaaaaaaaaaaaa [{'id': 170651, 'answer': 'Clara Barton', 'question': 'Pre-Red Cross in 1865, she set up a Bureau of Records to help search for missing soldiers', 'value': 800, 'airdate': '2015-01-09T20:00:00.000Z', 'created_at': '2022-12-30T21:04:22.067Z', 'updated_at': '2022-12-30T21:04:22.067Z', 'category_id': 20843, 'game_id': 4778, 'invalid_count': None, 'category': {'id': 20843, 'title': "this one's for the ladies", 'created_at': '2022-12-30T21:04:20.503Z', 'updated_at': '2022-12-30T21:04:20.503Z', 'clues_count': 5}}]
# [17/May/2023 06:46:20] "GET /home?page=7 HTTP/1.1" 200 16461
        values = Question.objects.create(
            body=a[0].get('question'),
            answer=a[0].get('answer'),
            question_value=a[0].get('value'), )
        values.save()

    else:
        print('An error has occurred.')
    return render(request, 'spa_table/home.html', queryset)





class Values_tableListView(ListView):
    model = Values_table
    template_name = 'spa_table/home.html'

    # print('___________1_____________')

    # print('___________2_____________')

# https://faint-adasaurus-4bc.notion.site/web-Python-adf33211e9cc4d6b9ec2c0c619ecab31
