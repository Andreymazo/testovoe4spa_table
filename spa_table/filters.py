import django_filters
from django_filters import OrderingFilter

from spa_table.models import Values_table


# https://django-filter.readthedocs.io/en/stable/guide/usage.html
class Values_tableFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains')#iexact
    # name = django_filters.CharFilter(lookup_expr='iexact')

    # name = django_filters.CharFilter(lookup_expr='gt')
    # name = django_filters.CharFilter(field_name='name')
    distance__gt = django_filters.NumberFilter(field_name='distance', lookup_expr='gt')
    # data__gt = django_filters.NumberFilter(field_name='data', lookup_expr='gt')
    # quantity__lt = django_filters.NumberFilter(field_name='quantity', lookup_expr='lt')

    # name__name = django_filters.CharFilter(lookup_expr='icontains')
    # order_by('name')

    def filter_queryset(self, queryset):
        """
        Не нашел в django-filters ничего проще ,чем переписать кверисет ,чтобы отсортировать по имени, но вот так сортирует
        """

        queryset=Values_table.objects.all().order_by('name')
        return queryset

    class Meta:
        model = Values_table
        ordering = ('name',)
        fields = ['name', 'distance']
        # , 'data', 'quantity'

