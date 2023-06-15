from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView

from spa_table import views
from spa_table.apps import SpaTableConfig
from spa_table.views import render_api_question, \
    TableListView, CustomUserLogin, CustomAuthToken, tz3_users, change_audio, search  # , filter_js
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# TableListView, RregisterView, CustomAuthToken,CustomPasswordResetView, change_audio,SignupAPIView,
# , Values_tableListView SignupView,
# https://jkaylight.medium.com/django-rest-framework-authentication-with-dj-rest-auth-4d5e606cde4d
app_name = SpaTableConfig.name

urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('login/', CustomUserLogin.as_view(), name='login'),
    path('register/', views.sign_up, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', TableListView.as_view(), name='tz1'),
    path('tz1_1/', search, name='tz1_1'),
    path('tz1/', TableListView.as_view(), name='tz1'),
    path('tz2/', render_api_question, name='tz2'),
    path('tz3/', tz3_users, name='tz3'),
    path('audio/', change_audio, name='audio'),
    path('api-token-auth/', CustomAuthToken.as_view()),

]
