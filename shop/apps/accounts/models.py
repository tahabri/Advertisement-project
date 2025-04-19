from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin  
from django.db import models
from utils import FileUplode
class CustoumUserManager(BaseUserManager):
    def create_user(self,mobile_number, activate_code=None,email='',family="",name="",image=None,password=None,):  
        if not mobile_number:
            raise ValueError('باید شماره موبایل وجود داشته باشد')
        user=self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            family=family,
            name=name,  
            activate_code=activate_code  ,
            # image_name=image
        )
        user.set_password(password)  
        user.save(using=self._db)
        
        return user
        
    def create_superuser(self, mobile_number,email,family,name,password=None,):
        user=self.create_user(
           mobile_number=mobile_number,
            email=self.normalize_email(email),
            family=family,
            name=name,   
            password=password
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user 
# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):
    mobile_number=models.CharField(max_length=11,verbose_name='شماره موبایل',unique=True)
    email=models.EmailField( max_length=200,blank=True)
    name=models.CharField(max_length=50,verbose_name='نام',blank=True)
    # file_uplode=FileUplode('images','profile')
    # image_name=models.ImageField(upload_to=file_uplode.uplode_to,verbose_name='تصویر ',)
    family=models.CharField(max_length=50,verbose_name='فامیلی',blank=True)
    activate_code=models.CharField(max_length=100,verbose_name='کد اکتیو',blank=True,null=True)
    data_rigister=models.DateField(default=timezone.now)
    is_active=models.BooleanField(default=False,verbose_name='فعال بودن')    
    is_active_sms=models.BooleanField(default=False,verbose_name='فعال بودن') 
    is_admin=models.BooleanField(default=False,verbose_name='ادمین بودن')  
    USERNAME_FIELD = 'mobile_number'  # تعیین فیلد ایمیل به عنوان فیلد نام کاربری  
    REQUIRED_FIELDS = ['email','name','family',]  # فیلدهای ضروری در زمان ساخت کاربر 
    objects=CustoumUserManager() 
    #--------------------
    @property
    def is_staff(self):
        return self.is_admin 

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'
class SendSms(models.Model):  
    user = models.OneToOneField(CustomUser, verbose_name="کاربر", on_delete=models.CASCADE)  
    sms_code = models.PositiveIntegerField(verbose_name='اسمس کد', null=True, blank=True)  
    date = models.DateTimeField(default=timezone.now,)  # زمان ایجاد شیء  

    def __str__(self):  
        return f"SMS Code: {self.sms_code} for {self.user.mobile_number}" 
class Employer(models.Model):
    user= models.OneToOneField(CustomUser, verbose_name="کاربر", on_delete=models.CASCADE)  
    workplace=models.TextField(verbose_name='ادرس محل کار')
    fields_of_work=models.TextField(verbose_name="در چه چیز هایی کار می کند")
    is_acitve=models.BooleanField(default=False,verbose_name='فعال بودن')    
    def __str__(self):
        return f"{self.user}"