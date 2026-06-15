from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Role

class RegisterSerializer(serializers.ModelSerializer):
    '''RegisterSerializer use model User and in it required username, email, password, confirm_password '''

    confirm_password = serializers.CharField(min_length=8, write_only=True)

    class Meta :
        model = User 
        fields = ['id', 'first_name','last_name','username', 'email', 'password', 'confirm_password', 'date_joined', 'last_login']
        read_only_fields =['id', 'date_joined', 'last_login']
        extra_kwargs= {

            'password' : {

            'write_only' : True,

            },

        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('اسم المستخدم مستخدم سابقا بالفعل ')
        return value 

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('الايميل مستخدم سابقا بالفعل ')
        return value

    def validate_password(self, value):
        try :#####
            validate_password(value)
        except DjangoValidationError as e :
            raise serializers.ValidationError({"password" : e.messages})
        return value #ترجع قيمة الباسوورد لاسم الدالة اذن قد استخدم الباسورد بعد التاكد ب self.validate_password


    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password and confirm_password and password != confirm_password :
            raise serializers.ValidationError('من فضلك تاكد من تطابق كلمة المرور')
        return data


    ###سؤال لماذا لا نستخدم save ولو استخدمناها كيف نكتبها وهل create شبه save في form وال model 
    ##لان save داخل الview تستدعي create, update ,,,,,,note create >> return user, update>>return insatnce 
    ##save تعمل تلقائي في ModelSerializer ولكن لو عاوز اعمل حاجة يبقي اعمل الدالة دي ولو serializer.Serializer لازم تعملها ااو تعملها في view 
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user =User.objects.create_user(**validated_data)#لازم  create_user لانها تحفظها مشفرة ولو عملناها create لن تنفع معها authenticate  لانها تقارن نتائج تشفيرها 
        Role.objects.create(user =user )
        return user




class LoginSerializer(serializers.Serializer):
    """LoginSerializer has required fields :username,and password """

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True )





class ProfileSerializer(serializers.ModelSerializer):
    """Profile Serializer use User model and has fields:first_name, last_name, username, email, also username is read_only """

    class Meta :
        model = User 
        fields = ['first_name', 'last_name', 'username', 'email']
        read_only_fields = ['username']
    ##self.instance للوصول الي ال user
    def validate_email(self,value):
        if User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('هذا الايميل مستقدم بالفعل من فضلك ادخل ايميل مختلف ')
        return value 


