from django.shortcuts import render , get_object_or_404
from .models import Product
from .filters import ProductFilter
from django.core.paginator import Paginator 
# Create your views here.

def products_list(request):
    ''' view function to list all products '''
    
    all_products = Product.objects.filter(available=True)
    products_filter = ProductFilter(request.GET ,queryset=all_products)
    filtered_products = products_filter.qs
    #paginator
    # 1. نعلم الpaginator 
    paginator  = Paginator(filtered_products, 4)
    
    # 2. نجيب الصفحة 
    page_number = request.GET.get('page', 1)
    
    # 3. ندي الصفحة لل paginator 
    products = paginator.get_page(page_number) # get_page >>> try, except     
   #يوجد طرق اخري يدوية وlistview 


    context = {
    'products' : products , 
    'products_filter' : products_filter ,   ##for form 
    #'filtered_products' : filtered_products ,
    'request' : request,
    }
    
    return  render(request, 'products/products_list.html', context)
    
    
    
    
def product_details(request, slug):
    ''' view function to show every product '''
    
    product = get_object_or_404(Product, slug=slug , available=True)
             
    related_products = Product.objects.filter(available=True).exclude(id=product.id)[:4]        
    
    context = {
    'product' : product,
    'related_products' : related_products,     
    }
    
    return render(request, 'products/product_details.html', context)
    