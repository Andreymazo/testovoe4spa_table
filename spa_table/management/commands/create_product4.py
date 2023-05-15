from django.core.management import BaseCommand

from price.models import Product, Category, CustomUser


class Command(BaseCommand):


    def handle(self, *args, **options):## Две функции креате, одна менеджерская, с ней увеличиваем прайс
        prod_lst = ['Grude Oile 355', 'Brent very best oil item']##lssns for 1st Course
        for i in prod_lst:
            product = Product.objects.create(
                user=CustomUser(pk=1),
                product_name=i,
                category=Category(pk=1),
                product_description="Wondeful things",
                price_value=10

            )

            product.save()


    # prod_lst = ['Grude Oile 355', 'Brent very best oil item']  ##lssns for 1st Course
    # for i in prod_lst:
    #     product = Product.objects.create_product(
    #         user_id=1,
    #         product_name=i,
    #         category_id=1,
    #         product_description="Wondeful things",
    #         price_value=10
    #
    #     )

        # product.save()

