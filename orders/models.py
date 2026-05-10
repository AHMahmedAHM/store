from django.db import models
from django.contrib.auth.models import User
from  products.models import Product
# Create your models here.



class Order(models.Model):
    
    STATUS=(
    ('pending', 'في الانتظار'),
    ('paid', 'تم الدفع'),
    ('shipped', 'تم الشحن'),
    ('delivered', 'تم التوصيل'),
    ('canceled', 'تم الالغاء'),
    ('failed','فشل الدفع'),
    ('refunded','تم الاسترداد')
    )         
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_index=True, related_name = 'order')
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20 )
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    def  get_total_cost(self):
        return sum( item.get_item_cost()    for item in self.items.all()  )
        
    def __str__(self):
        return f'order from {self.user.username}'
        
    class Meta :
        ordering = ['-created_at']
        
        
        
        
class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items' , db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items' , db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    quantity = models.PositiveIntegerField(default=1)
    
    
    def get_item_cost(self):
        return self.price * self.quantity
        
    def __str__(self):
        return f'order item for{self.product.name}'
            