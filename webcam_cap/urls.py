from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path('', index),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
