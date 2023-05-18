import allauth
import requests
import names
from allauth.account import app_settings
from allauth.account.utils import complete_signup
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django_tables2 import SingleTableView
from rest_auth.app_settings import create_token, TokenSerializer
from rest_auth.models import TokenModel
from rest_auth.registration.app_settings import register_permission_classes, RegisterSerializer
from rest_auth.registration.views import sensitive_post_parameters_m
from rest_auth.serializers import JWTSerializer
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from spa_table.models import Values_tableTable, Values_table, Question
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


class CustomAuthToken(ObtainAuthToken):

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


from django.utils.translation import ugettext_lazy as _


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = register_permission_classes()
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

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


#######################################################################3

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

        for i in range(1, 5):
            values = Values_table.objects.create(
                name=names.get_last_name(),
                quantity=randint(1, 100),
                distance=randint(1, 100), )
            values.save()
        queryset = Values_table.objects.all()

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

    return render(request, 'spa_table/home.html', queryset)


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
#         return render(request, 'spa_table/home.html', queryset)
#     return render(request, 'spa_table/home.html', queryset)
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
#     template_name = 'spa_table/home.html'

# <input type="number" value="{{number}}"  placeholder="Number of questions">

# https://faint-adasaurus-4bc.notion.site/web-Python-adf33211e9cc4d6b9ec2c0c619ecab31
