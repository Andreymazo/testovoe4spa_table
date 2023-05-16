import names
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django_tables2 import SingleTableView
from spa_table.models import Values_tableTable, Values_table
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


        global queryset
        if self.request.method == "GET":
            # for i in range(1, 10):
            #     values = Values_table.objects.create(
            #         name=names.get_last_name(),
            #         quantity=randint(1, 100),
            #         distance=randint(1, 100),)
            #     values.save()
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

        for i in range(1, 10):

            values = Values_table.objects.create(
                name=names.get_last_name(),
                quantity=randint(1, 100),
                distance=randint(1, 100), )
            values.save()
        queryset = Values_table.objects.all()

        return queryset


    # print('___________1_____________')


    # print('___________2_____________')

# https://faint-adasaurus-4bc.notion.site/web-Python-adf33211e9cc4d6b9ec2c0c619ecab31
