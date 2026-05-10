from django.db import models

# Create your models here.

class Category(models.Model):
    name= models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True )
    
    class Meta :
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
         return self.name
         
         
      







def upload_image(instance,filename):
    ''' this function for where the images media store  '''
    from datetime import datetime
    date=datetime.now()
    all_date = date.strftime('/%y/%m/%d')
    name,extension = filename.strip().split('.')
    return f'products/images/{all_date}/{instance.name}.{extension}'

class Product(models.Model):
    ''' class for show products and every product '''
    
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=60, unique=True,  blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to =upload_image)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, db_index=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1,  )
    available = models.BooleanField(default=True)
    published_at =models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)    

    class Meta :
        ordering = ['-published_at']
        verbose_name = 'product'
        verbose_name_plural = 'products'
        
        
    def save(self,*args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify 
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)            

    def __str__(self):
        return self.name    
                
    def get_absolute_url(self):
        ''' function for get url for every product'''
        from django.urls import reverse 
        return reverse('products:details', args=[self.slug])