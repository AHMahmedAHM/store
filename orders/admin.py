from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display=['user', 'phone', 'paid']
    list_link = ['user', 'phone']
    list_editable = ['paid']
    list_filter = ['status', 'created_at', 'updated_at', 'paid']
    search_fields = ['user', 'phone', 'payment_id', 'address', 'city']#لان الcity كتابة مش اختيارات للفلتر
    
admin.site.register(Order, OrderAdmin)

 
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order']
   # list_link = ['order']
    search_fields = ['order', 'product']
    list_filter = ['price'] 
    
admin.site.register(OrderItem, OrderItemAdmin )
                