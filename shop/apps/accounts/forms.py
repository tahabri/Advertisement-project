from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField,ReadOnlyPasswordHashWidget
class UserAdd(ModelForm):
    password1=forms.CharField(max_length=50,label='رمزعبور',widget=forms.PasswordInput)
    password2=forms.CharField(max_length=50,label='تکرار رمز عبور',widget=forms.PasswordInput)
    class Meta:
        model=CustomUser
        fields=['mobile_number','email','name','family']
    def clean_password2(self):
        data = self.cleaned_data["password"]
        data2 = self.cleaned_data["password2"]
        if data !=data2:
            raise ValidationError('تکرار رمز عبور با رمز عبور یکی نیست')
        return data2
    def save(self, commit =True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit == True:
            user.save()
        return user 
class UserChange(ModelForm):
    password=ReadOnlyPasswordHashField(help_text='کنید<a href=../password>کلیک</a>برای دیدن پسورد و عوض کردن ان ',label='رمزعبور',)
    class Meta:
        model=CustomUser
        exclude=[]