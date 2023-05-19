from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from spa_table.models import CustomUser


def set_verify_token_and_send_mail(new_user):
    """
        Деактивировать пользователя, установить токен и сроки жизни
        TODO: отправить письмо на почту со ссылкой
    """
    now = datetime.now(pytz.timezone(settings.TIME_ZONE))
    new_user.is_active = False
    new_user.verify_token = CustomUser.objects.make_random_password(length=20)
    new_user.verify_token_expired = now + timedelta(hours=72)
    new_user.save()

    link_to_verify = reverse('users:verify_email', args=[new_user.verify_token])
    # TODO: сделать красивое письмо
    # http://localhost:8000/users/verify/woefhowuhefoqihwefiqf/
    print("====================new", new_user.email)
    send_mail(
        subject='Подтвердите почту для BUBE-7',
        message=f'{settings.BASE_URL}{link_to_verify}',
        recipient_list=[new_user.email],
        from_email=settings.EMAIL_HOST_USER
    )
