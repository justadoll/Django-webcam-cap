from django.urls import path
from .views import pic_saver, create_link, get_log, del_log

urlpatterns = [
    path('create/', create_link),
    path('<str:p_link>/', pic_saver),
    path('log/<str:link>/', get_log),
    path('del/<str:link>/', del_log),
]

