import names
from django_tables2 import SingleTableView
from spa_table.models import Values_tableTable, Values_table
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

    queryset = Values_table.objects.all()
    template_name = "spa_table/Values_table_list.html"
    ordering = ('distance',)  # quantity, name
    table_pagination = {"per_page": 5}

# {% load django_tables2 %}
# {% render_table table %}
# https://faint-adasaurus-4bc.notion.site/web-Python-adf33211e9cc4d6b9ec2c0c619ecab31
