from django.shortcuts import render, redirect 
from django.urls import reverse
from django.db import transaction 
from django.contrib import messages
from .forms import OrderForm
from .models import OrderItem , Order
from products.models import Product
import paypalrestsdk
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail 


paypalrestsdk.configure({
    'mode' : 'sandbox', 
    'client_id' : settings.PAYPAL_CLIENT_ID, 
    'client_secret' : settings.PAYPAL_CLIENT_SECRET,
})
###كان ممكن وضعها في settings, AppConfig او هنا ولكن في بداية الملف 


@login_required
def orders_list(request):    
    
    context ={
        'orders' : Order.objects.filter(user=request.user).exclude(status='canceled'), 
        'orders_pending' : Order.objects.filter(user=request.user, status='pending'),
        'orders_delivered' : Order.objects.filter(user=request.user, status='delivered'),
        
    }
    
    return render(request, 'orders/orders_list.html', context)                
    

    
@login_required 
def order_create(request):
    
    order_items_list=[] 
    total = 0
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'السلة فارغة اذهب الي السلة للتاكد واضافة منتجات')
        return redirect('cart:details')
        
    #check from previous order >>one order
    previous_order = Order.objects.filter(user=request.user, status='pending').first()
    if previous_order :
        messages.error(request, 'من فصلك يوجد طلب سابق معلق اما تحذفه او يتم دفعه')
        return redirect('orders:orders_list')
    #start functions's aim'
    if request.method =='POST':        
        with transaction.atomic():
            form = OrderForm(request.POST)
            
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user   
                order.save()    
                request.session['order_id'] =order.id                   
               
                for product_id, quantity in cart.items() :
                    product = Product.objects.filter(id=int(product_id)).first() 
                    if not product :
                        raise ValueError(f'product id : {product_id} not found')
                    order_item = OrderItem.objects.create(
                        order = order, 
                        product = product, 
                        price=product.price, 
                        quantity = quantity, 
                    )      
                    order_items_list.append(order_item)                       
                
                #del request.session['cart']
                messages.success(request, 'تم انشاء الطلب بنجاح')
               # return redirect ('orders:details', order_id=order.id)#####
                return redirect('orders:order_confirm')
                
            else :
               messages.error(request,'فشل تسجيل الطلب تحقق من ادخال بيانات صحيحة') 
               
    else :
        for product_id, quantity in cart.items() :
             product = Product.objects.filter(id=int(product_id)).first() 
             total += float(product.price) * float(quantity) 
                    
        form = OrderForm()  
        
        
    context={
    'orders' : Order.objects.filter(user=request.user),
    'form' : form, 
    'cart' : cart, 
    'order_items_list' : order_items_list, 
    'total' : total, 
        }     
           
    return render(request,'orders/order_create.html', context )###      
    
    
     


@login_required                       
def order_confirm(request):    
    
    try:
        order_id = request.session.get('order_id')     
        order = Order.objects.get(id = order_id, user=request.user, status='pending')
        total = order.get_total_cost()
    except Order.DoesNotExist :
        messages.error(request, 'هذا الطلب  غير موجود ') 
        return redirect ('products:list')
    
    if order.paid :
        messages.warning(request, 'تم دفع هذا الطلب بالفعل ') 
        return redirect('products:list') 
        
    payment = paypalrestsdk.Payment({
        'intent' : 'sale' ,
        'payer' : {'payment_method':'paypal'},
        'redirect_urls' : {
            'return_url' : request.build_absolute_uri(reverse('orders:order_success')),
            'cancel_url' : request.build_absolute_uri(reverse('orders:order_cancel', args=[order.id])),
        },
        'transaction' : [{
            'amount' : {
                'total' : str(total),
                'currency' : settings.PAYPAL_CURRENCY,
            },
            'description' : f'طلب من موقعنا برقم {order_id}',
        }]
    })
    
    if payment.create():
        paypal_url = next((str(link.href) for link in payment.links if link.rel=='approval_url'), None)
        if not paypal_url :
            messages.error(request, 'فشل الحصول علي الرابط ')
            return redirect('orders:create')
            
        order.payment_id = payment.id
        order.save()      
          
        context ={
        'order' : order, 
        'total' : total, 
        'paypal_url' : paypal_url,
        }
        
#        pop=request.session.pop('cart',None)##تم تاخيرها الي هنا وسيتم نقلها الي ما بعد الدفع 
#        request.session.modified = True
        #if pop :
#            messages.info(request, 'تم حذف السلة بالكامل ') ##فكرة سيئة لانها قد تربك العميل كما انها قد تحتوي علي {} اذن الشرط لن يعمل لازم  if pop != None
        return render(request, 'orders/order_confirm.html', context)        
                
    else :
        messages.error(request, f'حدث خطا عند التوجه الي موقع الpaypal  الخطا هو{payment.error} اذا تكرر معاك تواصل مع الدعم  ')
        return redirect('orders:order_create')
        
       
#حتي تبعث webhook لازم اكتب الurl  اللي هيبعتوا عليه عندهم ولام احوش csrf  لانها POST  ومش بي#بعتوا csrf         
#@csrf_exempt
#@require_POST
#def paypal_webhook(request):
#     '''verify signature, event_type, payment_id, and change '''
#     
#     #كلم api  ب JsonResponse
#     
#     #اتاكد من توقيع paypal 
#     headers = request.headers
#     body = request.body     
#     webhook_id = settings.PAYPAL_WEBHOOK_ID
#     
#     try :
#         event = paypalrestsdk.WebhookEvent.verify(
#             headers = headers, 
#             body = body, 
#             webhook_id = webhook_id, 
#         )
#     except Exception as e :
#         return JsonResponse({'status': 'not_verified' , 'error' : f'{e}'}, status=400)    
#    # if not event :         
#     #    return JsonResponse({'status' : 'not valid'}, status=400)# in normal dj =200, in DRF=400
#     
#         
#    #اتاكد من حالة الطلب 
#    event_type = event.event_type
#    payment_id = event.resource.get('id')        
#    try :
#        order = Order.objects.get(payment_id=payment_id)            
#    except Order.DoesNotExist:
#        #messages.error(request, 'هذا الطلب غير موجود ')     ما ينفعشي مع api  
#        return JsonResponse({'status':'not found'},status=404)   
#    
#    if event_type == 'PAYMENT.SALE.COMPLETED' :
#        #اتاكد بعدها من رقم الطلب واجيبه       
#        if order.paid :
#            return JsonResponse({'status': 'already_paid'}) 
#        order.status='paid'
#        order.paid = True
#        order.save()
#        return  JsonResponse({'status' : 'succeed'},status=200)
#        
#    elif event_type == 'PAYMENT.SALE.DENIED' :             
#         order.status = 'failed'
#         order.save()
#         return JsonResponse({'status' : 'denied'}, status=200)   
#    
#    return JsonResponse({'status': 'not_completed_or_denied'})                  
         
@csrf_exempt
@require_POST
def paypal_webhook(request):
    #signature
    headers = request.headers
    body = request.body
    webhook_id = settings.PAYPAL_WEBHOOK_ID
    
    try:
        event = paypalrestsdk.WebhookEvent.verify(
            headers=headers,
            body=body,
            webhook_id=webhook_id
            )
    except Exception as e :
        return JsonResponse({'status' : 'not_verified', 'error' : str(e) }, status=400) 
        
    #requirements 
    payment_id = event.resource.get('id')
    event_type = event.event_type 
    paid_total_paypal = event.get('amount', {}).get('total', {})
    try:
        order = Order.objects.get(payment_id=payment_id)
        total = order.get_total_cost()
    except Order.DoesNotExist :
        return JsonResponse({'status' : 'not_found'}, status=400)    
    
    #change_order 
    if event_type == 'PAYMENT.SALE.COMPLETED' :
        if order.paid: #لان paypal  قد ترسل اكثر من مرة فلا استغل بياناتي
            return JsonResponse({'status' : 'already_paid'})
        if str(total) != paid_total_paypal :
            order.status = 'failed'
            order.save()
            return JsonResponse({'status' : 'amout mismatch'}, status=400)   
             
        order.status='paid' 
        order.paid=True
        order.save()   
        #del request.session['cart']  لاني اتعامل مع api وليس المتصفح
        
        return JsonResponse({'status' : 'succeed'})
        
    elif event_type == 'PAYMENT.SALE.DENIED' :
        if order.status == 'failed' :
            return JsonResponse({'status' : 'already_failed'})
        order.status ='failed'
        order.save()
        return JsonResponse({'status' : 'denied'})          
        
    return JsonResponse({'status' : 'not_completed_or_denied'})      
  
@login_required   
@require_POST
def order_cancel(request, order_id):
    
    ######مش محتاج تاكيد لانه مش هيصل للدالة بدونه
    #if not order_id:
#        messages.error(request, 'هذا الطلب اصبح  غير موجود ')
#        return redirect('products:list')
    #get order and check    
    try:
        order = Order.objects.get(id=order_id, user = request.user)
    except Order.DoesNotExist:
        messages.error(request, 'هذا الطلب اصبح غير موجود ') 
        return redirect('orders:orders_list')       
    #change order after check
    if order.status in ['paid', 'shipped', 'delivered'] :
        messages.warning(request, 'لا تسطيع الغاء الطلب الان')
        return redirect('orders:orders_list')
    elif order.status in ['failed', 'canceled'] :
        messages.info(request, 'هذا الطلب ملغي  بالفعل ')
        return redirect('orders:orders_list')
    elif order.status =='pending' and order.payment_id :
          messages.info(request, 'هذا الطلب جاري دفعه بالفعل ') 
          return redirect('orders:orders_list')    
          
    order.status = 'canceled'
    order.save()
    messages.success(request, 'تم  الغاء هذا الطلب  اذا كنت انت لم تلغيها تواصل معنا ')
    
    return redirect('orders:orders_list') 
 
    
    
@login_required           
def order_success(request):
            
    order_id = request.session.get('order_id', None)
    if not order_id :
        messages.error(request, 'معذرة طلبك غير موجود اذا كنت لا تعرف ذلك تواصل مع الدعم')
        return redirect('orders:orders_list')
        
    order = Order.objects.get(id=order_id, user=request.user)    
    if order.paid:
        messages.success(request, 'تم بنجاح دفع الطلب')
        
        send_mail(
            subject = 'اهلا بك  هذا اختبار انت في الطريق الصحيح',
            message = 'لا تقلق الله معك انت ان شاء الله تحاول اي نعم تقصر لكن لا تخف الله معك وستصل ان شاء الله لكن اجتهد واستمر ',
            from_email = settings.DEFAULT_FROM_EMAIL, 
            recipient_list = [order.user.email],
            fail_silently = False,       
        )
        # delete cart and order_id  pop or check and delete
        if 'cart'  in request.session:
            del request.session['cart']
        request.session.pop('order_id', None)
        
        
    elif not order.paid:
        if order.payment_id :
            messages.info(request, 'تم استلام طلبك سيتم تأكيد الدفع من ال paypal')
            messages.warning(request, 'من فضلك راجع طلبك باستمرار وان تاخر تواصل مع الدعم الفني ')            ###لحسن يجي هنا وييكون status=fail
        elif not order.payment_id:
            messages.warning(request, 'لم يتم الدفع بعد يمكنك العودة لصفحة الدفع ')
            messages.warning(request, 'من فضلك راجع طلبك باستمرار وان تاخر تواصل مع الدعم الفني ')    ###لحسن يجي هنا وييكون status=fail
            return redirect('orders:order_confirm')    
    return redirect('orders:orders_list')       