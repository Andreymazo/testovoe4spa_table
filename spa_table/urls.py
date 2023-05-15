from django.urls import path

from spa_table.views import TableListView

urlpatterns = [
               path('', TableListView.as_view(), name='Values_table_list')]#({'get': 'list'})
