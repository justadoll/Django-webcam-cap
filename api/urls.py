from django.urls import path
from .views import pic_saver

urlpatterns = [
    path('<str:p_link>/', pic_saver),
]

