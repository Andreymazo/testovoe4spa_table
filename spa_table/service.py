# accounts.utils
import datetime
import jwt
from django.conf import settings


def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=55),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')#.decode('utf-8')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')

    return refresh_token

#https://dev.to/a_atalla/django-rest-framework-custom-jwt-authentication-5n5

# from django.shortcuts import render
# from .forms import GeeksForm
#
#
# def handle_uploaded_file(f):
#     with open('media / musics/' + f.name, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#         # Create your views here.
#
#
# def home_view(request):
#     context = {}
#     if request.POST:
#         form = GeeksForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES["geeks_field"])
#     else:
#         form = GeeksForm()
#     context['form'] = form
#     return render(request, "home.html", context)
# from django import forms
#
#
# class GeeksForm(forms.Form):
#     name = forms.CharField()
#     geeks_field = forms.FileField()

