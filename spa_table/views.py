import os
import pydub
import requests
import names
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import QuerySet
from django.shortcuts import render, redirect

from django_tables2 import SingleTableView
from spa_table.forms import SigninForm, RegisterForm
from spa_table.models import Question, Values_table, Values_tableTable, \
    CustomUser
from random import randint


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from spa_table.service import generate_access_token


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



from django.contrib.auth import authenticate, login


class CustomUserLogin(LoginView):
    template_name = 'spa_table/registration/login.html'
    form_class = SigninForm


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'spa_table/registration/register.html', {'form': form})
    # qwert123asd
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        # form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
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

    return render(request, 'spa_table/users.html', queryset)


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

                return render(request, 'spa_table/users.html', queryset)
            print('Загрузите аудиофайл формата wav')

    else:
        return redirect('spa_table:login')
