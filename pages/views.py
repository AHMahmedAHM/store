from django.shortcuts import render
from products.models import Product
# Create your views here.


def index(request):
    latest_products = Product.objects.filter(available=True)[:5]
    
    context ={
    'latest_products' : latest_products, 
    }
    
    return render(request, 'pages/index.html', context)