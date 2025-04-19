from rest_framework import serializers
from .models import *
from jalali_date import datetime2jalali, date2jalali
class AdvertisementSerializer(serializers.ModelSerializer):  
    status = serializers.SerializerMethodField(read_only=True)  # فیلد جدید برای وضعیت  
    time=serializers.SerializerMethodField(read_only=True)
    class Meta:  
        model = Advertisement  
        exclude=["register_date","update_date","is_active"] # اضافه کردن فیلد status به خروجی  
         
    def get_status(self, obj):  
        return obj.is_active


    def get_time(self,obj):
        jalali_join = datetime2jalali(obj.register_date).strftime('%y/%m/%d _ %H:%M:%S')
        return jalali_join
        
    def validate_time(self, value):  
        
        return value  
    def create(self, validated_data):
        
        return Advertisement.objects.create(**validated_data)