from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
class SmsSerializer(serializers.Serializer):
    sms_code=serializers.CharField()
    def validate_sms_code(self,value):
        try:
            
            return int(value)
        except:
            raise serializers.ValidationError("باید عدد باشد")
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =CustomUser
        exclude=("activate_code","user_permissions","groups",)
        extra_kwargs={
            
        }
       
class UserWithTokenSerializer(UserSerializer):
    access=serializers.SerializerMethodField(read_only=True)
    re_password=serializers.CharField(write_only=True)
    class Meta:
        model =CustomUser
        exclude=['user_permissions','groups',]
        extra_kwargs={
            "password":{"write_only":True}
        }
    
    def __init__(self, *args, **kwargs):
        self.instance=kwargs.get("instance",None)
        return super(UserSerializer, self).__init__(*args, **kwargs)
       
    def get_access(self,obj):
        token=RefreshToken.for_user(obj)
        return str(token.access_token)
    def create(self, validated_data):
        
        del validated_data['re_password']
        
        user=CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])  
        user.save()
        return user
    def validate(self, attrs):
        data= super().validate(attrs)
        if self.instance == None:
            if data['password']!=data['re_password']:
                
                raise serializers.ValidationError("پسسورد و تکرار پسورد باید مثل هم باشند")
            return data
        if "password" in data:  
            if data.get('re_password') and data['password'] != data['re_password']:  
                raise serializers.ValidationError("پسورد و تکرار پسورد باید مثل هم باشند")  
        return data
    def update(self, instance, validated_data):
        
        instance.name=validated_data.get('name',instance.name)
        instance.family=validated_data.get('family',instance.family)
        if "password" in validated_data:  
            if validated_data.get('re_password') and validated_data['password'] != validated_data['re_password']:  
                raise serializers.ValidationError("پسورد و تکرار پسورد باید مثل هم باشند")  
            
            # حذف re_password از validated_data  
            validated_data.pop('re_password', None)  
            instance.set_password(validated_data["password"])  
        instance.save() 
        return instance
#________________________________________________________________________________
class EmployerSerializers(serializers.ModelSerializer):
    class Meta:
        model=Employer
        exclude=()
    
    def validate(self, attrs):
        # اعتبارسنجی‌های اضافی می‌توانند اینجا اضافه شوند
        
        return super().validate(attrs)
    def create(self, validated_data):
        return Employer.objects.create(**validated_data)