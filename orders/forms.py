from django import forms 
from .models import Order 

class OrderForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    
    class Meta :
        model = Order
        fields =['name', 'address', 'phone','city' ]
        
        
        widgets = {
        'name' : forms.TextInput(attrs={
        'type' : 'text' ,
        'class' : 'form-control' ,
        'rows' : 2 ,
        
        }),
        'phone' : forms.TextInput(attrs={'type':'tel'}),
            } 