
from django.urls import path, include, re_path

from spa_table.apps import SpaTableConfig
from spa_table.views import TableListView, render_api_question, RegisterView, CustomAuthToken  # , Values_tableListView

app_name = SpaTableConfig.name

urlpatterns = [
               path('', TableListView.as_view(), name='tz1'),
               # path('tz1/', render_api_question),
               path('tz2/', render_api_question, name='tz2'),
               path('api-auth/', include('rest_framework.urls')),
               # path('rest-auth/registration/', include('rest_auth.registration.urls'), name='tz3'),
               path('registration/', RegisterView.as_view(), name='tz3'),
               path('api-token-auth/', CustomAuthToken.as_view())
# RegisterView
]
#from django.contrib.auth import views
