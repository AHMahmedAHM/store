from django.urls import path
from . import api_views


urlpatterns =[
    #روابط المصادقة
    path('register/', api_views.api_register, name='api_register'),
    path('login/', api_views.api_login, name='api_login'),
    path('refresh_token/', api_views.api_refresh_token, name='api_refresh_token'),
    path('logout/', api_views.api_logout, name='api_logout'),

    #روابط الملف الشخصي
    path('profile/', api_views.api_profile, name='api_profile'),
]