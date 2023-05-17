from django.urls import path

from spa_table.views import TableListView, render_api_question#, Values_tableListView

urlpatterns = [
               path('', TableListView.as_view(), name='Values_table_list'),
               path('home', render_api_question, name='home'),
               # path('home', Values_tableListView.as_view(), name='home'),
]#({'get': 'list'})
