from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from store.serializers import ProductSerializer
from store.models import Product


class ProductsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ProductList(ListAPIView):
    """
    Doc string appears on view:
    Product List
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('name', 'description')
    # http://127.0.0.1:8000/api/v1/products/?limit=1&offset=1
    # This is because we have specified the limit as 3 which indicates that the
    # page size is 1 and an offset of 1 means that the starting point of this page
    # should be after the first 1 rows in the result-set.
    pagination_class = ProductsPagination

    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale', None)
        if on_sale is None:
            return super().get_queryset()
        queryset = Product.objects.all()
        # http://127.0.0.1:8000/api/v1/products/?on_sale=true
        # Note. modify sale start date in db
        if on_sale.lower() == 'true':
            from django.utils import timezone
            now = timezone.now()
            return queryset.filter(
                sale_start__lte=now,
                sale_end__gte=now,
            )
        else:
            return queryset.filter(
                sale_end=None
            )
