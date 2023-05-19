
from django.urls import path, include, re_path
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView, LogoutView

from spa_table.apps import SpaTableConfig
from spa_table.views import render_api_question, CustomAuthToken, RregisterView, tz3, LoginView, \
    TableListView  # TableListView,
     # , Values_tableListView
#https://jkaylight.medium.com/django-rest-framework-authentication-with-dj-rest-auth-4d5e606cde4d
app_name = SpaTableConfig.name

urlpatterns = [
                   path('register/', RegisterView.as_view(), name='register'),
                   path('login/', LoginView.as_view(template_name='spa_table/login.html'), name='login'),# {'template_name': 'login.html'}),#template_name='login.html'
                   path('logout/', LogoutView.as_view(), name='logout'),
                   path('', TableListView.as_view(), name='tz1'),
                   path('tz1/', TableListView.as_view(), name='tz1'),
                   path('tz2/', render_api_question, name='tz2'),
                   path('tz3/', tz3, name='tz3'),
                   # path('api-auth/', include('rest_framework.urls')),
                   # path('rest-auth/registration/', include('rest_auth.registration.urls')),
                   # path('registration/', RregisterView.as_view(), name='tz3'),
                   path('api-token-auth/', CustomAuthToken.as_view()),

]

