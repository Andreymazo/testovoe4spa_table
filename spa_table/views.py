import os
import token
from datetime import datetime
from pathlib import Path

import allauth
import jwt
import pydub
import requests
import names
from allauth.account import app_settings
from allauth.account.utils import complete_signup
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView

from django.core.exceptions import ImproperlyConfigured
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponse, request, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django_tables2 import SingleTableView
from rest_auth.app_settings import create_token, TokenSerializer, LoginSerializer
from rest_auth.models import TokenModel
from rest_auth.registration.app_settings import register_permission_classes, RegisterSerializer
from rest_auth.registration.views import sensitive_post_parameters_m
from rest_auth.serializers import JWTSerializer
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from config.settings import SECRET_KEY
from spa_table.forms import SigninForm, SignupForm, CustomPasswordResetForm, RegisterForm, CustomUserForm
from spa_table.models import Question, Values_table, Values_tableTable, \
    CustomUser  # CustomUser, Values_tableTable, Values_table,
from random import randint

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# @receiver(post_save, sender=get_user_model())  #
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication

from spa_table.serializers import SignupSerializer
from spa_table.service import generate_access_token
from spa_table.templates.spa_table.service import set_verify_token_and_send_mail


class CustomAuthToken(ObtainAuthToken):  ## Без этой функции ДРФ не работает

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.utils.translation import ugettext_lazy as _


class SigninView():
    pass


from django.contrib.auth import authenticate, login


class CustomUserLogin(LoginView):
    template_name = 'spa_table/registration/login.html'
    form_class = SigninForm
    # def get_context_data(self, **kwargs):
    #     context = super(CustomUserLogin, self).get_context_data(self, **kwargs)
    #     token_exist = CustomUser.objects.get(self, **kwargs)
    #
    #     context.update({'token'})
    #     if CustomUser.token


# <a class="btn btn-link" href="{% url 'spa_table:password_reset' %}">Забыли пароль?</a>
#                <br>

class SignupView(CreateView):
    template_name = 'spa_table/registration/register.html'
    model = CustomUser
    form_class = SignupForm
    success_url = reverse_lazy('spa_table:register_success')

    def form_valid(self, form):
        print('___________________________')
        if form.is_valid():
            self.object = form.save()
            set_verify_token_and_send_mail(self.object)
        return super().form_valid(form)


def handle_uploaded_file(f):
    with open('media / musics/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'spa_table/registration/register.html', {'form': form})
    # qwert123asd
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        # form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            # print('iiiiiiiiiiiiiiiiiiiiiiiii')
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.token = generate_access_token(user)
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            return redirect('spa_table:tz2')
        else:
            return render(request, 'spa_table/registration/register.html', {'form': form})


# https://fahimirfan70.medium.com/user-creation-using-django-abstractbaseuser-and-login-using-jwt-web-authentication-5d9fbfdd14ed
# PyJWT==2.7.0
class SignupAPIView(APIView):
    permission_classes = []

    def post(self, request):
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)
        if password == confirm_password:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ''
            raise ValidationError(
                {'password_mismatch': 'Password fields didn not match.'})
        return Response(data, status=response)


# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'users/password_reset_form.html'
#     form_class = CustomPasswordResetForm
#     success_url = reverse_lazy('users:password_reset_done')
#     email_template_name = 'users/email_reset.html'
#     from_email = settings.EMAIL_HOST_USER


# def my_view(request):
#     username = request.POST.get("username")
#     password = request.POST.get("password")
#     user = authenticate(request, username=username, password=password)
#
#     if user is not None:
#         login(request, user)
#         return HttpResponse(
#                     redirect=redirect('spa_table:tz2'),)
#     else:
#         print('Error message')


# class LoginView(GenericAPIView):
#     """
#     Check the credentials and return the REST Token
#     if the credentials are valid and authenticated.
#     Calls Django Auth login method to register User ID
#     in Django session framework
#
#     Accept the following POST parameters: username, password
#     Return the REST Framework Token Object's key.
#     """
#     permission_classes = (AllowAny,)
#     serializer_class = LoginSerializer
#     token_model = TokenModel
#     template_name = 'spa_table/login.html'
#     # https: // www.django - rest - framework.org / api - guide / reverse /
#     @sensitive_post_parameters_m
#     def dispatch(self, *args, **kwargs):
#
#         return super(LoginView, self).dispatch(*args, **kwargs)
#
#     def process_login(self):
#         django_login(self.request, self.user)
#
#     def get_response_serializer(self):
#         if getattr(settings, 'REST_USE_JWT', False):
#             response_serializer = JWTSerializer
#         else:
#             response_serializer = TokenSerializer
#         return response_serializer
#
#     def login(self):
#         self.user = self.serializer.validated_data['user']
#
#         if getattr(settings, 'REST_USE_JWT', False):
#             #########################################
#             # self.token = jwt_encode(self.user)
#             print('0000000000000000000000000000000', self.user)
#             self.token = jwt_encode(self.user)
#
#         else:
#             self.token = create_token(self.token_model, self.user,
#                                       self.serializer)
#
#         if getattr(settings, 'REST_SESSION_LOGIN', True):
#             self.process_login()
#
#     def get_response(self):
#         serializer_class = self.get_response_serializer()
#
#         if getattr(settings, 'REST_USE_JWT', False):
#             print('___________1___________')
#             data = {
#                 'user': self.user,
#                 'token': self.token,
#                 'tz2': reverse('tz2', request=request)
#                 # reverse("news-year-archive", args=(year,)))
#             }
#             serializer = serializer_class(instance=data,
#                                           context={'request': self.request})
#         else:
#             serializer = serializer_class(instance=self.token,
#                                           context={'request': self.request})
#
#         print('__________2____________', serializer.data)#__________2____________ {'key': '0bb908a04d33dea15f237497478dd408a3afd81c'}
#
#
#         response = Response(serializer.data, status=status.HTTP_200_OK)
#         # if getattr(settings, 'REST_USE_JWT', False):
#         #     from rest_framework_jwt.settings import api_settings as jwt_settings
#         #     if jwt_settings.JWT_AUTH_COOKIE:
#         #         from datetime import datetime
#         #         expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
#         #         response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
#         #                             self.token,
#         #                             expires=expiration,
#         #                             httponly=True)
#         return response
#
#     def post(self, request, *args, **kwargs):
#         # redirect_url = request.GET.get('redirect_url')
#
#         self.request = request
#         print('___________3___________', self.request.data)#____________3___________ <QueryDict: {'csrfmiddlewaretoken': ['4g5QcEnpoTviPeE1VPzdms57M4UMEGey1AxmCe7KVAkZYXWyzoyaFKZeKqYWXzQJ'], 'username': ['andr344eymazo33'], 'email': ['q21w@qw.ru'], 'password': ['qwert123asd']}>
#
#         self.serializer = self.get_serializer(data=self.request.data,
#                                               context={'request': request},
#                                               )
#         self.serializer.is_valid(raise_exception=True)
#
#         self.login()
#         return self.get_response()
#
# # class LoginView(APIView):
# #     permission_classes = (AllowAny,)
#
#     # def post(self, request, *args, **kwargs):
#     #     username = request.data['username']
#     #     password = request.data['password']
#     #
#     #     user = authenticate(username=username, password=password)
#     #
#     #     if user is not None:
#     #         payload = {
#     #             'user_id': user.id,
#     #             'exp': datetime.now(),
#     #             'token_type': 'access'
#     #         }
#     #
#     #         user = {
#     #             'user': username,
#     #             'email': user.email,
#     #             'time': datetime.now().time(),
#     #             'userType': 10
#     #         }
#     #
#     #         token = jwt.encode(payload, SECRET_KEY).decode('utf-8')
#     #         return JsonResponse({'success': 'true', 'token': token, 'user': user})
#     #
#     #     else:
#     #         return JsonResponse({'success': 'false', 'msg': 'The credentials provided are invalid.'})

class RregisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = register_permission_classes()
    token_model = TokenModel

    # template_name = 'spa_table/login.html'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RregisterView, self).dispatch(*args, **kwargs)

    success_url = reverse_lazy('spa_table:tz1')

    def get_response_data(self, user):

        if app_settings.EMAIL_VERIFICATION == \
                app_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            return JWTSerializer(data).data
        else:
            return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # success_url = reverse_lazy('spa_table:tz1')
        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)
        ####################################################################33
        # response = super(RegisterView, self).create(request, *args, **kwargs)
        # # here may be placed additional operations for
        # # extracting id of the object and using reverse()
        # return HttpResponseRedirect(redirect('spa_table:tz1'))
        # # redirect('spa_table:tz1'),
        # return HttpResponse(self.get_response_data(user),
        #                 redirect(request.META.get('HTTP_REFERER', '/')),
        #                 status=status.HTTP_201_CREATED,
        #                 headers=headers)

    # def get_success_url(self, request):
    #     # global response
    #     if self.request.method == 'POST':
    #         # form = AdverForm(request.POST, request.FILES)
    #         # if form.is_valid():
    #         #     form.instance.user = request.user
    #         #     form.save()
    #         response = redirect('/')
    #     # return response

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)
        # success_url = reverse_lazy('spa_table:tz1')
        complete_signup(self.request._request, user,
                        app_settings.EMAIL_VERIFICATION,
                        None)
        return user


def generate_values():
    for i in range(1, 10):
        values = Values_table.objects.create(
            name=names.get_last_name(),
            quantity=randint(1, 100),
            distance=randint(1, 100),
        )
        values.save()
        queryset = Values_table.objects.all()
        return queryset


from django_tables2 import tables


class TableListView(SingleTableView):
    model = Values_table
    table_class = Values_tableTable
    # generate_values()
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

        for i in range(1, 10):
            generate_values()

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

    return render(request, 'spa_table/users.html', queryset)


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
#         return render(request, 'spa_table/users.html', queryset)
#     return render(request, 'spa_table/users.html', queryset)
# <form action="/login/" method="POST">
#   <input type="text" name="keyword" placeholder="Search query">
#   <input type="number" name="results" placeholder="Number of results">
# </form>

def proverka_unik(a: str):
    HH = []
    H = Question.objects.all()
    index = 0
    try:
        question = Question.objects.get(pk=1).body
    except Question.DoesNotExist:
        question = None
    # print(question)
    while len(H) - index > 1:
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
#     template_name = 'spa_table/users.html'

# <input type="number" value="{{number}}"  placeholder="Number of questions">

# https://faint-adasaurus-4bc.notion.site/web-Python-adf33211e9cc4d6b9ec2c0c619ecab31

def tz3_users(request):
    number_form = NumberQuestion(request.POST)
    queryset = {'object_list': CustomUser.objects.all,
                'number_form': number_form}

    return render(request, 'spa_table/users.html', queryset)


# https://stacktuts.com/how-to-replace-overwrite-update-change-a-file-of-filefield-in-django
def change_audio(request):
    if request.user.is_authenticated:

        filepath1 = f'media/{request.user.file_wav}'
        filepath2 = f'media/{request.user.pk}.mp3'
        queryset = {'object_list': CustomUser.objects.all}

        if request.user.file_wav:
            if str(request.user.file_wav).endswith('.wav') is True:
                t = CustomUser.objects.get(pk=request.user.pk)
                sound = pydub.AudioSegment.from_file(filepath1)
                sound.export(filepath2, format="mp3")
                from django.core.files import File

                if os.path.isfile(str(t.file_mp3)):
                    # if t.file_mp3.exists():

                    current_file_path = t.file_mp3.path
                    os.remove(current_file_path)
                with open(filepath2, 'rb') as f:
                    file_obj = File(f)
                    t.file_mp3.save(f'new_file{request.user.pk}.mp3', file_obj, save=True)

                # from django.core.files.storage import default_storage
                # from django.core.files.base import ContentFile

                # my_object = MyModel.objects.get(pk=1)
                # old_file = my_object.my_file_field
                # new_file = ContentFile("new file content")
                # filename = default_storage.save(old_file.name, new_file)
                # my_object.my_file_field = filename
                # my_object.save()
                # https: // stacktuts.com / how - to - replace - overwrite - update - change - a - file - of - filefield - in -django

                # queryset.update({f'{t.file_mp3}': f'{sound.export(filepath2, format="mp3")}'})

                return render(request, 'spa_table/users.html', queryset)
            print('Загрузите аудиофайл формата wav')

    else:
        return redirect('spa_table:login')

# Добавление аудиозаписи, POST:
# Принимает на вход запросы, содержащие уникальный идентификатор пользователя, токен доступа и аудиозапись в формате wav;
# Преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет их в базе данных;
# Возвращает URL для скачивания записи вида http://host:port/record?id=id_записи&user=id_пользователя.
# Доступ к аудиозаписи, GET:
# Предоставляет возможность скачать аудиозапись по ссылке из п 2.2.3.
