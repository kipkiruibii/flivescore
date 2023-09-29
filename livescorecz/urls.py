from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('livescore_admin/', admin.site.urls),
    path('', include('livescore.urls')),
]
