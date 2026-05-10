from django.urls import path 
from . import views 

app_name = 'orders'

urlpatterns =[
    path('',views.orders_list, name='orders_list' ),
    path('order_create/', views.order_create, name='order_create'),
    path('order_confirm/', views.order_confirm, name='order_confirm'),
    path('order_success/', views.order_success, name='order_success'),
    path('order_cancel/<int:order_id>/', views.order_cancel, name='order_cancel'),
    #path('order_details/<int:order_id>/', views.order_details, name='order_details'),
    
]