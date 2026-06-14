from rest_framework import serializers 
from .models import Product 


class ProductSerializer(serializers.ModelSerializer):
    """ProductSerializer for Product model and in it name, descrption, price, category, stock"""
    class Meta :
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock']