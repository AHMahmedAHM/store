from django.shortcuts import render,redirect ,get_object_or_404
from  products.models import Product
from django.contrib import messages 
from django.views.decorators.http import require_POST

# Create your views here.


def cart_details(request):
    ''' view function to list user cart  '''
    
    cart = request.session.get('cart', {}) ## علشان لو دخل للتفاصيل من غير ما يضيف
    cart_items =[]
    total_price = 0
    total_quantity=0
    
    for product_id , quantity in cart.items() :
        product = get_object_or_404(Product, id=product_id)        
        total_price += product.price * quantity
        total_quantity += quantity
        
        cart_items.append({
        'product_id' : product_id,
        'product' : product,
        'quantity' : quantity,
        'item_price' : product.price * quantity, 
        })      
        
    #cart_items.append({'total_price':total_price})
    
    context = {
    'cart_items' : cart_items, 
    'total_price' : total_price,    
    'total_quantity' : total_quantity, 
    'cart_counts' : len(cart_items),
    }      
    
    return render (request, 'cart/cart_details.html', context)                                                
    
                                         
                                                                              
                                                                                                                                                        
    
@require_POST ### لا تحتاج   if request.method =="POST"  
def cart_add(request, product_id):
    ''' view function to add products to cart '''
    
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    quantity =int(request.POST.get('quantity', 1))
    
    if str(product_id) in cart.keys():
        cart[str(product_id)]  += quantity
    else :
        cart[str(product_id)] = quantity
        
    request.session['cart'] = cart ##لضمان تحديث ال cart         
    request.session.modified = True 
    
    messages.success(request, f'تم اضافة المنتج بنجاح{product.name}')  
    
    return redirect('cart:details' )


    
    
    

@require_POST
def cart_remove(request, product_id):
    ''' view function to remove priducts '''
    
    cart = request.session.get('cart',{})
    if not cart :
        messages.error(request, 'لا يوجد منتجات في السلة من فضلت اضف منتجات في البداية') 
        return redirect('products:details')
         ##رسالة لا يوجد منتجات

    if str(product_id) in cart.keys():
        del  cart[str(product_id)]
        request.session['cart'] = cart
    else :
        messages.error(request, f'المنتج غير موجود الرجاء التأكد او التواصل معنا ')  ##رسالة المنتج لا يوجد
        
    return redirect('cart:details')
  




@require_POST
def cart_update(request, product_id):
    '''view function to update cart for both increase or decrease'''
    
    cart = request.session.get('cart', {})
    action = request.POST.get('action')
    product_id = str(product_id)
    
    if product_id in cart.keys():
        if action == 'increase':
            cart[product_id] += 1
        elif action == 'decrease':
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                del cart[product_id]
        else:
            messages.error(request, 'حدث خطأ من فضلك اعد تحميل الصفحة')  # رسالة حدث خطا
            return redirect('cart:details')
    
    request.session['cart'] = cart
    return redirect('cart:details')    
    
                                                             