from rest_framework import serializers

from store.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'sale_start', 'sale_end')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['is_on_sale'] = instance.is_on_sale()
        data['current_price'] = instance.current_price()
        return data

# D:\Akshay\LessonsLearnt\django-REST-API\demo>python manage.py shell
# IPython 7.16.1 -- An enhanced Interactive Python. Type '?' for help.
#
# In [1]: from store.models import Product
#
# In [2]: from store.serializers import ProductSerializer
#
# In [3]: product = Product.objects.all()
#
# In [4]: product = Product.objects.all()[0]
#
# In [5]: serializer = ProductSerializer(product)
#
# In [6]: serializer.data
# Out[6]: {'id': 1, 'name': 'Mineral Water Strawberry!', 'description':
# 'Natural-flavored strawberry with an anti-oxidant kick.',
# 'price': 1.0, 'sale_start': None, 'sa
# le_end': None, 'is_on_sale': False, 'current_price': 1.0}
