from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from store.serializers import ProductSerializer
from store.models import Product


class ProductList(ListAPIView):
    """
    Doc string appears on view:
    Product List
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)

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
