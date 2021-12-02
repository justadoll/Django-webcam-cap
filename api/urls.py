from django.urls import path
from .views import pic_saver, create_link, get_log

urlpatterns = [
    path('create/', create_link),
    path('<str:p_link>/', pic_saver),
    path('log/<str:link>/', get_log),
]

