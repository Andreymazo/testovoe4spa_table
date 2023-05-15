from django.core.management import BaseCommand

from spa_table.models import Values_table


class Command(BaseCommand):

    def handle(self, *args, **options):
        crss = ['Oil', 'Wood']

        for i in crss:
            values = Values_table.objects.create(
                name=i,
                quantity=5,
                distance=2
            )
            values.save()
