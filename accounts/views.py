from django.shortcuts import render, redirect
from django.contrib.auth import login, logout #authenticate
from django.contrib import messages
from .forms import CustomRegisterForm, CustomLoginForm, UserProfileForm
from .models import Role
from django.contrib.auth.decorators import login_required

# Create your views here.
#🎯 ملخص: ما تعلمته من هذا التمرين

#1. الفرق بين RegisterForm و LoginForm

# RegisterForm LoginForm
#يرث من UserCreationForm AuthenticationForm
#يحتاج request؟ ❌ لا ✅ نعم
#طريقة الحصول على المستخدم form.save() form.get_user()
#يحتاج Meta؟ ✅ نعم ❌ لا

#2. تدفق العمل

#```
#Register: POST → form.is_valid() → form.save() → login() → redirect
#Login:    POST → form.is_valid() → form.get_user() → login() → redirect
#```
################

def register(request):
    
    if request.method=='POST':

        form = CustomRegisterForm(request.POST) #كتير عملت Meta اذن ياخد كله
        if form.is_valid():
            user =form.save()
            login(request, user)
            #اعمل object الاول 
            Role.objects.create(name='customer', user=user)
            #user.role.name ='customer'#####دي طريقة تغيير لو ال object موجود 
            messages.success(request, 'تم بنجاح تسجيل مستخدم جديد')
            return redirect('products:list')

        else:
            messages.error(request,'البيانات غير صحيحة من فضلك ادخل بيانات صحيحة ' )         
    
    else:
        if  request.user.is_authenticated: 
            messages.warning(request, 'انت مسجل دخول بالفعل')
            return redirect('login')

        form =CustomRegisterForm()

    return render(request, 'registration/register.html', {'form' : form})    



def login_view(request):
    if request.method=='POST':
        form = CustomLoginForm(request, data=request.POST)#فورم قليل اذن no Meta  اذن نعمل data
        if form.is_valid():
            user= form.get_user()
            login(request,user)
            messages.success(request, 'تم بنجاح تسجيل الدخول')
            
            remember_me = form.cleaned_data.get('remember_me')
            if remember_me :
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)                
            
            return redirect('products:list')
        else:
            messages.error(request, 'تم ادخال بيانات غير صحيحة')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form':form})      
    
    
    
def logout_view(request):
    if request.method =='POST':
        logout(request)
        messages.warning(request, 'تم تسجيل الخروج بنجاح') 
        return redirect('login')
    return render(request, 'registration/logged_out.html')
    
    
    
@login_required    
def profile(request):
    if request.method=='POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم الحفظ بنجاح')
            return redirect('profile')
        else :
            messages.error(request, 'تم ادخال بيانات غير صحيحة ')
            
    else:
        form =UserProfileForm(instance=request.user)
        
    return render(request, 'registration/profile.html', {'form':form})                