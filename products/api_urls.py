from django.urls import path 
from . import api_views 

urlpatterns =[
    path('', api_views.api_products_list, name='api_products_list'),
    path('add_product/', api_views.api_add_product, name='api_add_product'),
    path('update_product/<int:product_id>/', api_views.api_update_product, name='api_update_product'),
    path('delete_product/<int:product_id>/', api_views.api_delete_product, name='api_delete_product'),
    
]