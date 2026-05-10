import django_filters 
from django import forms
from .models import Category, Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset = Category.objects.all(),
        label = 'الفئة' ,
        empty_label = 'كل الفئات',
        to_field_name = 'name',         
    )
    
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label = 'الاسم',
        widget =forms.TextInput(attrs={'type':'text', 'class':'form-control', 'placeholder':'ابحث عن اي حروف داخل اسم المنتج' }),
    )
    description = django_filters.CharFilter(
        field_name = 'description', 
        lookup_expr= 'icontains', 
        label ='الوصف',
        widget =forms.Textarea(attrs={'class':'form-control','rows':'2', 'type':'text', 'placeholder':'ابحث عن اي كلمات داخل الوصف'}),
    )
    price_gte = django_filters.NumberFilter(
        field_name='price', 
        lookup_expr='gte',
        label='السعر أكبر من ',
        widget = forms.NumberInput(attrs={'class':'form-control', 'placeholder':'اكتب سعر وسنأتي به وبالاغلي منه '})
    )
    price_lte = django_filters.NumberFilter(
        field_name = 'price', 
        lookup_expr = 'lte', 
        label = 'السعر اقل من ',
        widget = forms.NumberInput(attrs={'class':'form-control', 'placeholder':'اكتب سعر وسناتي به وبالاقل منه '})
    )
    published_at =django_filters.DateFilter(
        lookup_expr='gte',
        label ='التاريخ من ',
        widget=forms.DateInput(attrs={'class':'form-control', 'type':'date', 'placeholder':'اختر التاريخ وسنأتي به وبالاحدث'})
    )
    
    
    
    #date
    class Meta :
        model = Product 
        fields =[]
            