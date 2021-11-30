from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('<str:g_link>/', index),
]
