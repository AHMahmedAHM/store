from django.contrib import admin
from.models import Product, Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin) :
    #fields =
    #exclude =
    list_display = ['name', 'slug']
    list_display_links = ['slug']
    link_display_editable = ['name']
    
admin.site.register(Category, CategoryAdmin)



class ProductAdmin(admin.ModelAdmin):
    '''class for admin product class  '''
    list_display = ['name', 'price', 'available' , 'stock']
    list_display_links = ['name']
    list_editable = ['price', 'available', 'stock']
    list_per_page = 20
    list_filter = ['price','category', 'stock', 'available', 'published_at', 'updated_at']
    search_fields = ['name', 'description', 'price', ]
    
admin.site.register(Product, ProductAdmin)


