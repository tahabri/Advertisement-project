
from random import randint
from django.shortcuts import render

# Create your views here.
from datetime import timedelta
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count  
from utils import send_sms
from django.contrib.auth import authenticate, login 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import *
from rest_framework.decorators import api_view,permission_classes
from django.core.cache import cache  
# Create your views here.
class MyTokenObtainPairSerialaizer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data= super().validate(attrs)
        if self.user.is_active == False or self.user.is_active_sms == False:
            raise serializers.ValidationError("حساب کاربری شما فعال نیست ")
        user=UserWithTokenSerializer(self.user,many=False).data
        for k,v in user.items():
            data[k]=v
        return data        
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerialaizer
#Register------------------------------------ثبت نام-------------------------------
@api_view(["POST"])
def register(request):
    
    code = randint(100000, 999999)  
    # try:
    ser_data=UserWithTokenSerializer(data= request.POST)
    
    if ser_data.is_valid():
        
        user=ser_data.create(ser_data.validated_data)   
    else:
        user=CustomUser.objects.get(mobile_number=request.POST['mobile_number'])
        print(user.is_active)
        if user.is_active== False and user.is_active_sms == False:
            pass
        else:
            return Response(data=ser_data.errors)    
        
       
    # except:
    #    
    try:
        # ایجاد کد SMS و ذخیره زمان فعلی  
            SendSms.objects.create(  
                user=user,  
                sms_code=code,  
                date=timezone.now()  # ذخیره زمان فعلی  
            )  
    except:
            sms=SendSms.objects.get(  
                user=user,  
                  
                  # ذخیره زمان فعلی  
            )  
            sms.sms_code=code
            sms.date=timezone.now()
            sms.save()
    request.session['mobile_number']=user.mobile_number
    message = f"کاربر محترم این کد {code} شما برای ورود است "  
    send_sms(message, int(request.session['mobile_number']))  
    return Response(data="پیامک شما ارسال شد")
#_________________________________________________________
@api_view(["POST"])
def check_sms(request):
    current_time = timezone.now()
        
    user = CustomUser.objects.get(mobile_number=request.session['mobile_number'])  
    sms = SendSms.objects.get(user=user)  
    expiry_time = sms.date + timedelta(minutes=1)  # زمان انقضای کد  
    print(expiry_time,current_time)
    # ایجاد کلید یکتا برای آدرس IP  
    ip_address = request.META.get('REMOTE_ADDR')  
    login_attempts_key = f"login_attempts_{ip_address}"  

        # بررسی تعداد تلاش‌های ناموفق  
    attempts = cache.get(login_attempts_key, 0)  

    if attempts >= 5:  
        return Response(data="حساب کاربری قفل شده است. تعداد تلاش‌های ناموفق بیش از حد مجاز بوده است.")

    ser_data = SmsSerializer(data=request.POST)  
    
    if current_time<= expiry_time:  
        if ser_data.is_valid():  
            if sms.sms_code == ser_data.validated_data['sms_code']:  
                
                del request.session['mobile_number'] 
                ser_user=UserWithTokenSerializer(instance=user,many=False) 
                user.is_active_sms=True
                user.is_active=True
                user.save()
                return Response(data=ser_user.data)  # به صفحه مناسب تغییر دهید  
            else:  
                cache.set(login_attempts_key, attempts + 1, timeout=3600)  # ثبت تلاش ناموفق  
                return Response(data="اشتباه است")  
        else:
            return Response(ser_data.errors)
    else:  
        return Response(data="کد منقضی شده است.")
            

        # اگر فرم معتبر نباشد  
#end Register------------------------------------ پایان ثبت نام-------------------------------   
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_uesr(request):
    ser_data=UserSerializer(instance=request.user,many=False)
    return Response(data=ser_data.data)
    
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_uesr(request):
    ser_data=UserWithTokenSerializer(instance=request.user,data=request.POST,partial=True)
    if ser_data.is_valid():
        ser_data.update(request.user,ser_data.validated_data)
        return Response(data=ser_data.data)
    return Response(data=ser_data.errors)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_employer(request):
    data={
        "workplace":request.POST.get("workplace",None),
        "fields_of_work":request.POST.get("fields_of_work",None),
        "user":request.user.id
    }
    ser_data=EmployerSerializers(data=data,context={"request":request})
    
    
    if ser_data.is_valid():
        ser_data.create(ser_data.validated_data)
        
        return Response(data=ser_data.data, status=201)
    return Response(data=ser_data.errors, status=400)
#finish