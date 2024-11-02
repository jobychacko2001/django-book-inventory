import django_filters
from .models import Inventory


class InventoryFilter(django_filters.FilterSet):
    class Meta:
        model = Inventory
        fields = {
            'title': ['icontains'],
            'author': ['icontains'],
            'genre': ['exact'],
        }
