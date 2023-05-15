from django.core.management import BaseCommand

from price.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = CustomUser.objects.create(
            email= 'andreymazo@mail.ru',
            is_superuser=True,
            is_staff=True
        )
        user.set_password('qwert123asd')
        user.save()