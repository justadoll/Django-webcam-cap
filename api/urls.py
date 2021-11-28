from django.urls import path
from .views import pic_saver

urlpatterns = [
    path('', pic_saver),
]

