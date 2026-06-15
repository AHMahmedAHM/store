from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, authenticate
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken


##ملحوظة request.data.get() لا تاخذ من return Response  بتاعتي انما يبعتها العميل فلازم توحد الالفاظ اللي بتبعتها علشان تعرف تاخد وتدي

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    """ api_register for new user and user RegisterSerializer"""

    serializer  = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()##هنا تستدعي create  او لو ModelSerializer اذن تلقائي
        login(request, user)
        refresh = RefreshToken.for_user(user)
        refresh['role'] =user.role.name
        refresh.access_token['role'] = user.role.name

        return Response({
            'success' : True,
            'message' : 'تم انشاء مستخدم جديد بنجاح',
            'serializer' : serializer.data ,
            'refresh_token' : str(refresh), 
            'access_token' : str(refresh.access_token),

        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message' : 'البيانات المدخلة غير صالحة ',
        'error' : serializer.errors ,

    }, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):##يحتاج هذه الدالة ٧ ايام 
    """api_login not for a new user and user LoginSerializer and the period continue 7 days """

    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(): ##لن احفظ شئ لانه بالفعل محفوظ في قاعدة البيانات مجرد التاكد
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password') ##serializer.validated_data for data ,,,,, for user  serializer.insatnce
        user = authenticate(request, username = username, password=password)
        if user is None :
            return Response({'success':False, 'message' : 'بيانات الدخول غير صحيحة '}, status=status.HTTP_400_BAD_REQUEST) ##  وهذا افضل امنيا من قول المستخدم غير موجود 
        
        login(request, user)
        
        refresh = RefreshToken.for_user(user)
        refresh['role'] =user.role.name
        refresh.access_token['role'] = user.role.name


        
        return Response({
            'success' : True, 
            'message' : 'تم تسجيل دخول بنجاح',
            'refresh_token' : str(refresh),
            'access_token' : str(refresh.access_token),
            'serializer' : serializer.data ,
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message' : 'البيانات المدخلة غير صالحة ',
        'error' : serializer.errors ,
        
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny]) #استخدمت لاي حد لان الدالة سوف تعمل في حالة انتهي تسجيل الدخول العادي
def api_refresh_token(request):##للحصول علي access_token جديد
    """api_refresh_token is to get access token that continue 30 minutes """

    refresh = request.data.get('refresh_token', None)

    if refresh is None :
        return Response({'message' : 'refresh_token عير موجود '}, status=status.HTTP_400_BAD_REQUEST)
    
    try :
        refresh = RefreshToken(refresh) ##حتي يتاكد منه
        user = request.user
        refresh['role'] =user.role.name
        refresh.access_token['role'] = user.role.name


    except :
        return Response({'message':"refresh_token غير صالح من فضلك اعد تسجيل الدخول"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': True, 
        'message' : 'تم الحصول علي access_token بنجاح',
        ##'refresh_token' :str(refresh), مش محتاج ارسلها لانها لم تتغير
        'access_token':str(refresh.access_token),

    }, status=status.HTTP_200_OK)






@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def api_profile(request):#للعرض والتحديق الجزئي والكلي
    """api_profile to GET, PUT, PATCH user's profile """

    if request.method =='GET':
        serializer = ProfileSerializer(instance =request.user)
        return Response(serializer.data,status=200)
    
    is_partial = request.method =='PATCH'
    #خارج ال if
    serializer = ApiProfileSerializer(instance=request.user, data=request.data, partial=is_partial)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'success':True,
            'message' :'تم تحديث ملف مستخدم بنجاح',
            'user' : serializer.data,     ##الا بنفع  user.data
        })
    
    return Response({
        'success': False,
        'message' : 'البيانات المدخلة غير صالحة ',
        'error' : serializer.errors ,        
    }, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):## يتم وضع ال token في  blacklist
    """api_logout for expery refresh_token and log user out """

    refresh = request.data.get('refresh_token',None)

    if refresh is None :
        return Response({'message':'refresh_token  غير موجود '}, status=status.HTTP_400_BAD_REQUEST)
    
    #افحصه واتاكد منه
    try :
        refresh = RefreshToken(refresh)
        refresh.blacklist()
    except Exception as e:
        return Response({'message':'refresh_tokenغير صالح ', 'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'message':'تم تسجيل الخروج بنجاح'}, status=status.HTTP_200_OK)


