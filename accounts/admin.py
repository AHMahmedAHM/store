from django.contrib import admin
from .models import Role

# Register your models here
class RoleAdmin(admin.ModelAdmin):
    fields_list =['name']
    fields_link =['name']

admin.site.register(Role, RoleAdmin)