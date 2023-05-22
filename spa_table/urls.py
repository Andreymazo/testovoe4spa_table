from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView

from spa_table import views
from spa_table.apps import SpaTableConfig
from spa_table.views import render_api_question, \
    TableListView, CustomUserLogin, SignupView, CustomAuthToken, SignupAPIView, tz3_users, change_audio
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# TableListView, RregisterView, CustomAuthToken,CustomPasswordResetView, change_audio,
# , Values_tableListView
# https://jkaylight.medium.com/django-rest-framework-authentication-with-dj-rest-auth-4d5e606cde4d
app_name = SpaTableConfig.name

urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register2/', views.sign_up, name='register2'),
    # path('register_w_token/', views.RegisterView, name='register_w_token'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    # path('login/', LoginView.as_view(template_name='spa_table/login.html'), name='login'),# {'template_name': 'login.html'}),#template_name='login.html'
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', TableListView.as_view(), name='tz1'),
    path('tz1/', TableListView.as_view(), name='tz1'),
    path('tz2/', render_api_question, name='tz2'),
    path('tz3/', tz3_users, name='tz3'),
    # path('api-auth/', include('rest_framework.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('registration/', RregisterView.as_view(), name='tz3'),
    path('api-token-auth/', CustomAuthToken.as_view()),
    # path('login/', my_view, name='login'),
    path('login/', CustomUserLogin.as_view(), name='login'),
    # path('', SigninView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignupView.as_view(), name='register'),
    path('audio/', change_audio, name='audio'),#change_audio,
    # path('register/success/', SignupSuccessView.as_view(), name='register_success'),
    # path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),

    # path('password/reset/<uidb64>/confirm/<token>/', CustomPasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password/reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #
    # path('verify/<str:token>/', verify_email, name='verify_email'),
    #
    # path('simple/reset/', simple_reset_password, name='simple_reset'),
    #
    # path('profile/', UserProfileView.as_view(), name='profile')
]
