from rest_framework import serializers

from store.models import Product, ShoppingCartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = ('product', 'quantity')


class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'price', 'sale_start', 'sale_end',
            'is_on_sale', 'current_price', 'cart_items',
        )

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data

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

## Serializer that shows model relationships using SerializerMethodField()
# import json
# from store.models import *
# from store.serializers import *
# product  = Product.objects.all().first()
# cart = ShoppingCart()
# cart.save()
# item = ShoppingCartItem(shopping_cart=cart, product=product, quantity=5)
# item.save()
# serializer = ProductSerializer(product)
# print(json.dumps(serializer.data, indent=2))

# ---output---
# {
#   "id": 2,
#   "name": "Mineral Water Raspberry",
#   "description": "Flavoured with raspberry, loaded with anti-oxidants.",
#   "price": 2.0,
#   "sale_start": null,
#   "sale_end": null,
#   "is_on_sale": false,
#   "current_price": 2.0,
#   "cart_items": [
#     {
#       "product": 2,
#       "quantity": 5
#     }
#   ]
# }
