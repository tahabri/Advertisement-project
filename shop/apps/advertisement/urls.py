from . import views
from django.urls import path,include

urlpatterns = [
    path('view/',views.Advertisementview.as_view(),name='view'),
    path('add_advertisement/',views.create_advertisement,name='add_advertisement'),
    path('advertisement/<int:pk>/',views.get_advertisement,name='advertisement'),
    path('my_advertisement/',views.get_my_advertisement,name='my_advertisement'),
]
