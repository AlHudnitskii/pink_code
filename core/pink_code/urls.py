from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/main/', include('core.main.urls')),
   path('api/auth/', include('core.auth_.urls')),
   path('api/interpreter/', include('core.code_interpreter.urls')),
   path('api/u/', include('core.users.urls')),
]
