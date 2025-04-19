from datetime import timedelta
from django.db import models
from jalali_date.fields import JalaliDateTimeField
from apps.accounts.models import CustomUser
from utils import FileUplode
from django.utils import timezone
from django.core.exceptions import ValidationError  

# Create your models here.
class TypeAdvertisement(models.Model):
    name=models.CharField(verbose_name="نام نوع", max_length=50)
    price=models.IntegerField(verbose_name="هزینه",)
    def __str__(self):
        return f" نوع {self.name}"
class PriceAdvertisement(models.Model):
    price=models.IntegerField(verbose_name=' قیمت به ازای هر روز',)#قیمت به ازای هر روز
    def save(self, *args, **kwargs):  
        if self.pk is None and PriceAdvertisement.objects.exists():  
            raise ValidationError('تنها یک شیء از PriceAdvertisement مجاز است.')  
        super().save(*args, **kwargs) 
    def __str__(self):
        return f"روز{self.time}"
class Advertisement(models.Model):
    title=models.CharField(max_length=20,default="")
    user=models.ForeignKey(CustomUser, verbose_name="کاربر", on_delete=models.CASCADE)
    time_day=models.PositiveIntegerField(default=1)
    type=models.ForeignKey(TypeAdvertisement, verbose_name="نوع", on_delete=models.CASCADE)
    file_uplode=FileUplode('images','Advertisement')
    image_name=models.ImageField(upload_to=file_uplode.uplode_to,verbose_name='تصویر ',)
    discription=models.TextField(verbose_name='توضیحات')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت فعال/غیر فعال')
    # مقداردهی خودکار تاریخ درج  
    state=models.TextField(verbose_name='مهارت',default="برنامه نویسی")
    register_date = models.DateTimeField(verbose_name='تاریخ درج',default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)  
    price=models.PositiveBigIntegerField(verbose_name="قیمت تبلیغ",default=0)
    def __str__(self):
        return f"{self.user}--{self.time_day}--{self.type}"
   
    def is_valid_this_time(self):  
        register_date = self.register_date  
        expiry_time = register_date + timedelta(days=self.time)  
        current_time = timezone.now()  # صدا زدن تابع به جای ارجاع به آن  
        
        if expiry_time >= current_time:  
            return True  
        return False
    def get_price(self):
        price=0
        for pr in PriceAdvertisement.objects.all():
            price=pr.price
        type=self.type.price
        return (price*self.time_day)+type
# class Bar(models.Model):
#     objects = jmodels.jManager()
#     name = models.CharField(max_length=200)
#     date = jmodels.jDateField()

#     def __str__(self):
#         return "%s, %s" % (self.name, self.date)


# class BarTime(models.Model):
#     objects = jmodels.jManager()
#     name = models.CharField(max_length=200)
#     datetime = jmodels.jDateTimeField()

#     def __str__(self):
#         return "%s, %s" % (self.name, self.datetime)