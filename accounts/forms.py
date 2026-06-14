from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

#for register form  
class CustomRegisterForm(UserCreationForm):
    
    phone=forms.CharField(max_length=20, 
        widget=forms.TextInput(attrs={'type':'tel', 'class':'form-control', 'placeholder':'01xxxxxxxxx'  }))
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('هذا الايميل موجود بالفعل')
        return email 
        
    def clean_username(self) :
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('اسم المستخدم موجود بالفعل')
        return username
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) != 11:
            raise forms.ValidationError('ادخل رقم هاتف مكون من 11 رقم ')
        #if phone and phone[0:1] != '01':
            #raise forms.ValidationError('لابد ان يبدأ رقم الهانف ب "01"  ')
        return phone
        
    def save(self, commit=True,*args,**kwargs ):
        user = super().save(commit=False,*args,**kwargs,)
        #phone for profile
        if commit:
            user.save()
            #وضع phone ما يوضع يدوي يحفظ يدوي       
            return user                                                                
    
    class Meta :
        model = User
        fields=['first_name', 'last_name', 'username','email','phone']
        widgets ={
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'اكتب اسمك الاول'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'اكتب اسمك الاخير هنا'}),
            'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'اختر اسم مستخدم'}),
            'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'ادخل ايميلك هنا'}),        }
            


class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(initial =False , widget=forms.CheckboxInput(attrs={'class':'form-check-box'})) ##no default in forms but in models 
    
    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username_or_email or not password:
            raise forms.ValidationError('تحقق من ملء كل الحقول')
            #return cleaned_data
        
        if '@' in username_or_email :
            try:
                user = User.objects.get(email=username_or_email)
                username_or_email = user.username
            except User.DoesNotExist:
                raise forms.ValidationError('هذا الايميل غير موجود')
                
        user = authenticate(username=username_or_email, password=password)
        if user is  None:
            raise forms.ValidationError('اسم المستخدم او كلمة المرور غير صحيحة')
                  
        self.user_cache = user ##in views user=form.get_user() instead of  user=request.user 
        #تقريبا لا يوجد request.user  ولكن هستدعي form.get_user() علشان تتاكد هي من المصادقة            
                    
        return cleaned_data            
            
   
                     
                                                         
class UserProfileForm(forms.ModelForm): #no heritage from RegistrationForm بسبب منطق كلمة المرور
    phone = forms.CharField(max_length=15, required=True, 
       widget=forms.TextInput(attrs={'type':'tel', 'placeholder':'01×××××××××','class':'form-control'}))
    class Meta :
        model =User
        fields =['first_name', 'last_name', 'username', 'email', 'phone']
        widgets ={
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'اكتب اسمك الاول'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'اكتب اسمك الاخير هنا'}),
            'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'اختر اسم مستخدم'}),
            'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'ادخل ايميلك هنا'}),        }
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id =self.instance.id####instance هو كائن ال user  وclass اذن الوصول ب . 
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError('هذا الايميل مستخدم بالفعل')
        return email
        
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and (len(phone) !=11 or not phone.startswith('01') ) :
            raise forms.ValidationError('من فضلك ادخل رقم هاتف مصري صحيح')
        return phone
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_id = self.instance.id 
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            raise forms.ValidationError('هذا اسم المستخدم موجود بالفعل ') 
        return username       