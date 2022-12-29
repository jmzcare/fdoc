from django_filters import rest_framework as filters

from .models import *


class Source_sectorFilter(filters.FilterSet):
    source_sector_index = filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('source_sector_index', 'sector_index'),
        ))
    class Meta:
        model = Source_sector  # 模型名
        fields = ['source_sector_index',]

class CustomerFilter(filters.FilterSet):
    customer_name = filters.CharFilter(field_name='customer_name',distinct=True)
    class Meta:
        model = Customer  # 模型名
        fields = ['customer_name',]
