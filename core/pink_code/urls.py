from django.contrib import admin
from django.urls import path, include


urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/main/', include('core.main.urls')),
   path('api/auth/', include('core.auth_.urls')),
   path('api/interpreter/', include('core.code_interpreter.urls')),
   path('api/users/', include('core.users.urls')),
]