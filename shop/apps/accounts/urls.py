from . import views
from django.urls import path,include

urlpatterns = [
    path('login/',views.MyTokenObtainPairView.as_view(),name='login'),
    path('register/',views.register,name='register'),
    path('check_sms/',views.check_sms,name='check_sms'),
    path("upadate_profile/",views.update_uesr,name='update_profile'),
    path("get_user/",views.get_uesr,name='get_user'),
    path("create_employer/",views.create_employer,name='create_employer'),
]