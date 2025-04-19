from datetime import timedelta
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import *
from .serializers import AdvertisementSerializer
from django.core.paginator import Paginator
from rest_framework.decorators import api_view,permission_classes
from django.db.models import Q
from django.db.models import Count  
from permissions import IsEmployer
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class Advertisementview(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        paginator_number = 2  
        current_time = timezone.now() 
        objects=Advertisement.objects.filter(Q(is_active=True)&Q(register_date__lte=current_time)).order_by('type','register_date')
        for obj in objects:
            if not obj.is_valid_this_time():
                obj.is_active=obj.is_valid_this_time()
                obj.save()
            
        
        objects=objects.filter(is_active=True)
        q=request.GET.get('q')
        if q :
            print('a')
            objects=objects.filter(title__contains=q)
        page_number = request.GET.get('page') 
        if page_number == None:
            page_number=1
        order=request.GET.get('order')
        order2=None
        if order:
            if order == "جدید ترین ":
                order2='-register_date'
                objects=objects.order_by(order2)
            elif order == "قدیمی ترین":
                order2="register_date"
                objects=objects.order_by(order2)
        else:
            pass
        state=order=request.GET.get('state') 
        if state :
            
            objects=objects.filter(state__contains=state)      
        product_count=objects.count() 
        list_show=[]
        i=paginator_number  
        paginator = Paginator(objects, paginator_number)       
        page_obj = paginator.get_page(page_number)  
        serializer=AdvertisementSerializer(instance=page_obj,many=True)
        return Response(data=serializer.data)
@api_view(["POST"])
@permission_classes([IsEmployer])
def create_advertisement(request):
    # user=models.ForeignKey(CustomUser, verbose_name="کاربر", on_delete=models.CASCADE)
    # time=models.ForeignKey(PriceAdvertisement, verbose_name="مدت زمان", on_delete=models.CASCADE)
    # type=models.ForeignKey(TypeAdvertisement, verbose_name="نوع", on_delete=models.CASCADE)
    try:
        type=TypeAdvertisement.objects.get(name=request.POST.get("type"))
    except:
        return Response(data="همچین نوعی وجود ندارد")
    time=int(request.POST.get("time_day"))
    price=0
    for pr in PriceAdvertisement.objects.all():
        price=pr.price
    data={
        "image_name":request.data.get("image_name"),
        "discription":request.POST.get("discription"),
        "state":request.POST.get("state"),
        "title":request.POST.get("title"),
        "user":request.user.id,
        "time_day":time,
        "type":type.id,
        "price":time*price,
        
        
        
    }
    ser_data=AdvertisementSerializer(data=data)
    if ser_data.is_valid():
        advertisement=ser_data.create(ser_data.validated_data)
        print(advertisement)
        ser_data=AdvertisementSerializer(instance=advertisement,many=False)
        return Response(data=ser_data.data)
    return Response(data=ser_data.errors)
@api_view(["GET"])
def get_advertisement(request,pk):
    try:
        obj=Advertisement.objects.get(pk=pk,is_active=True)
    except:
        return Response(data="Not found 404")
    ser_data=AdvertisementSerializer(instance=obj,many=False)
    return Response(data=ser_data.data)
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def get_my_advertisement(request):
    objs=Advertisement.objects.filter(user=request.user)
    if objs.exists():
        ser_data=AdvertisementSerializer(instance=objs,many=True)
        return Response(data=ser_data.data)
    return Response(data="هیچی ندارید شما")