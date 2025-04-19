from django.contrib import admin
from django.forms import JSONField
from .models import *
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
# Register your models here.

@admin.register(PriceAdvertisement)

@admin.register(TypeAdvertisement)


    

	
@admin.register(Advertisement)  
class AdvertisementAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):  
    list_display = ['get_created_jalali']  
    
    @admin.display(description='تاریخ ایجاد', ordering='register_date')  
    def get_created_jalali(self, obj):  
        return datetime2jalali(obj.register_date).strftime('%a, %d %b %Y %H:%M:%S') 
    
	
