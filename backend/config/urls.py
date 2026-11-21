from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('catalog.urls')), 
    path('api/auth/',include('accounts.urls')) #registration request POST http://127.0.0.1:8000/api/auth/register/
]